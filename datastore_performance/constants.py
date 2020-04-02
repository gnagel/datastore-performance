from __future__ import absolute_import

import csv
import logging
import math
import time
import uuid
from StringIO import StringIO
from collections import namedtuple
from contextlib import contextmanager

from google.appengine.ext import ndb

from datastore_performance import sql_api

_logger = logging.getLogger(__name__)

TestRunResult = namedtuple('TestRunResult', [
    'klass',
    'properties_count',
    'test_group',
    'row_count',
    'iteration_count',
    'total_milli_seconds',
    'avg_milli_seconds',
])

INSTANCES_TO_CREATE = 100
NUM_INSTANCES_TO_DESERIALIZE = 20
READ_ITERATIONS = 100


def model_classes():
    from datastore_performance import models
    model_classes = [
        models.PgModel10,
        models.DbModel10,
        models.NdbModel10,
        #
        models.DbExpando10,
        models.NdbExpando10,
        #
        models.PgModel100,
        models.DbModel100,
        models.NdbModel100,
        #
        models.DbExpando100,
        models.NdbExpando100,
    ]
    return model_classes


def create_result(model_class, test_group, seconds, iterations, row_count):
    if seconds is None:
        return TestRunResult(
            klass=model_class.__name__,
            properties_count=len(model_class._properties.keys()),
            test_group=test_group.value,
            row_count=None,
            iteration_count=None,
            total_milli_seconds=None,
            avg_milli_seconds=None,
        )

    avg_milli_seconds = (seconds * 1000 / float(iterations))
    avg_milli_seconds = int(avg_milli_seconds * 100) / 100.0
    return TestRunResult(
        klass=model_class.__name__,
        properties_count=len(model_class._properties.keys()),
        test_group=test_group.value,
        row_count=row_count,
        iteration_count=iterations,
        total_milli_seconds=math.floor(seconds * 1000),
        avg_milli_seconds=avg_milli_seconds,
    )


@contextmanager
def create_row(model_class):
    row = model_class()
    for property in row._properties.keys():
        setattr(row, property, str(uuid.uuid4()))
    model_class.put([row])

    key = _resolve_key(row)

    # Wait till the data syncs to Datastore
    while not filter(lambda x: x, model_class.get([key])):
        _logger.info("Waiting for %s models to appear ...", model_class.__name__)
        time.sleep(0.1)

    try:
        yield row, key
    finally:
        if not issubclass(model_class, sql_api.PgQueryMixin):
            model_class.delete([row])


@contextmanager
def create_rows(model_class, count):
    rows = []
    for _ in range(count):
        row = model_class()
        for property in row._properties.keys():
            setattr(row, property, str(uuid.uuid4()))
        rows.append(row)
    model_class.put(rows)

    # Wait till the data syncs to Datastore
    keys = map(_resolve_key, rows)
    while len(filter(lambda x: x, model_class.get(keys))) != len(rows):
        time.sleep(0.1)

    try:
        yield rows, keys
    finally:
        if not issubclass(model_class, sql_api.PgQueryMixin):
            model_class.delete(rows)


def _resolve_key(row):
    if issubclass(row.__class__, ndb.Model):
        return row.key
    if issubclass(row.__class__, sql_api.PgQueryMixin):
        return row._key
    else:
        return row.key()


def benchmark_fn(fn, num_iterations):
    try:
        start = time.time()
        for _ in range(num_iterations):
            fn()
        end = time.time()
        seconds = float(end - start)
        return seconds
    except NotImplementedError:
        # raise
        return None


def format_csv(results):
    rows = []
    for index, result in enumerate(results):
        klass = result.klass
        properties_count = result.properties_count
        test_name = result.test_group.split(': ')[0]
        test_description = ': '.join(result.test_group.split(': ')[1:])
        row_count = result.row_count
        iteration_count = result.iteration_count
        total_milli_seconds = result.total_milli_seconds
        avg_milli_seconds = result.avg_milli_seconds

        row = [
            test_name,
            test_description,
            klass,
            avg_milli_seconds,
            total_milli_seconds,
            properties_count,
            row_count,
            iteration_count,
        ]
        # Space the test groups apart
        if index > 0 and result.test_group != results[index - 1].test_group:
            rows.append([])
        rows.append(row)

    headers = [
        'Operation',
        'Description of test',
        'Model Name',
        'Avg Milliseconds per call',
        'Total Milliseconds all iterations',
        'Number of Columns',
        'Number of Rows',
        'Number of Iterations',
    ]
    return csv2string(headers, rows)


def csv2string(headers, rows):
    string_buffer = StringIO()
    writer = csv.writer(string_buffer)
    writer.writerow(headers)
    writer.writerows(rows)
    return string_buffer.getvalue().strip('\r\n').strip('\n')
