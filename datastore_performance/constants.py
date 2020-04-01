from __future__ import absolute_import

import csv
import time
import uuid
from StringIO import StringIO
from collections import namedtuple
from contextlib import contextmanager

from google.appengine.ext import ndb

from datastore_performance import models

TestRunResult = namedtuple('TestRunResult', [
    'klass',
    'properties_count',
    'test_group',
    'row_count',
    'iteration_count',
    'total_milli_seconds',
    'avg_milli_seconds',
])

DB_MODEL_CLASSES = [
    models.Model10,
    models.Model100,
    models.Expando10,
    models.Expando100,
]
NDB_MODEL_CLASSES = [
    models.NdbModel10,
    models.NdbModel100,
    models.NdbExpando10,
    models.NdbExpando100,
]
MODEL_CLASSES = DB_MODEL_CLASSES + NDB_MODEL_CLASSES

INSTANCES_TO_CREATE = 100
NUM_INSTANCES_TO_DESERIALIZE = 20
SERIALIZATION_ITERATIONS = 100
READ_ITERATIONS = 100


def create_result(model_class, test_group, seconds, iterations):
    return TestRunResult(
        klass=model_class.__name__,
        properties_count=len(model_class._properties.keys()),
        test_group=test_group.value,
        row_count=1,
        iteration_count=SERIALIZATION_ITERATIONS,
        total_milli_seconds=seconds,
        avg_milli_seconds=seconds / float(iterations),
    )


@contextmanager
def create_row(model_class):
    row = model_class()
    for property in row._properties.keys():
        setattr(row, property, str(uuid.uuid4()))
    model_class.put(row)

    key = _resolve_key(row)

    # Wait till the data syncs to Datastore
    while not model_class.get(key):
        time.sleep(0.5)

    try:
        yield row, key
    finally:
        model_class.delete(row)


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
        time.sleep(0.5)

    try:
        yield rows, keys
    finally:
        model_class.delete(rows)


def _resolve_key(row):
    if issubclass(row.__class__, ndb.Model):
        return row.key().to_old_key()
    else:
        return row.key()


def benchmark_fn(fn, num_iterations):
    start = time.time()
    for _ in range(num_iterations):
        fn()
    end = time.time()
    seconds = float(end - start)
    return seconds


def format_csv(results):
    rows = []
    for result in results:
        klass = result.klass
        properties_count = result.properties_count
        test_name = result.test_group.split(':')[0]
        test_description = ':'.join(result.test_group.split(':')[1:])
        row_count = result.row_count
        iteration_count = result.iteration_count
        total_milli_seconds = result.total_milli_seconds
        avg_milli_seconds = result.avg_milli_seconds

        row = [
            test_name,
            test_description,
            klass,
            properties_count,
            row_count,
            iteration_count,
            total_milli_seconds,
            avg_milli_seconds,
        ]
        rows.append(row)

    headers = [
        'test_name',
        'test_description',
        'klass',
        'properties_count',
        'row_count',
        'iteration_count',
        'total_milli_seconds',
        'avg_milli_seconds',
    ]
    return csv2string(headers, rows)


def csv2string(headers, rows):
    string_buffer = StringIO.StringIO()
    writer = csv.writer(string_buffer)
    writer.writerow(headers)
    writer.writerows(rows)
    return string_buffer.getvalue().strip('\r\n').strip('\n')
