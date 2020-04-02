from __future__ import absolute_import

import logging
import time
import uuid

import enum
from google.appengine.ext import ndb

from datastore_performance.constants import INSTANCES_TO_CREATE, NUM_INSTANCES_TO_DESERIALIZE, \
    create_result, create_row, create_rows, benchmark_fn, model_classes

_logger = logging.getLogger(__name__)

CRUD_ITERATIONS = 10


@enum.unique
class CrudTestGroups(enum.Enum):
    READ_SINGLE_ROW = 'Read Model: Fetch a single row'
    READ_MULTI_ROW = 'Read Model: Fetch {}x rows'.format(NUM_INSTANCES_TO_DESERIALIZE)
    READ_BULK = 'Read Model: Fetch {}x rows from the database at at time'.format(INSTANCES_TO_CREATE)
    READ_MISSING_BULK = 'Read Missing Model: Fetch {}x from the database that dont exist'.format(INSTANCES_TO_CREATE)

    ASYNC_READ_SINGLE_ROW = 'Async Read Model: Fetch a single row'
    ASYNC_READ_MULTI_ROW = 'Async Read Model: Fetch {}x rows'.format(NUM_INSTANCES_TO_DESERIALIZE)
    ASYNC_READ_BULK = 'Async Read Model: Fetch {}x rows from the database at at time'.format(INSTANCES_TO_CREATE)
    ASYNC_READ_MISSING_BULK = 'Async Read Missing Model: Fetch {}x from the database that dont exist'.format(
        INSTANCES_TO_CREATE)

    LAZY_READ_SINGLE_ROW = 'Lazy Read Model: Fetch a single row'
    LAZY_READ_MULTI_ROW = 'Lazy Read Model: Fetch {}x rows'.format(NUM_INSTANCES_TO_DESERIALIZE)
    LAZY_READ_BULK = 'Lazy Read Model: Fetch {}x rows from the database at at time'.format(INSTANCES_TO_CREATE)
    LAZY_READ_MISSING_BULK = 'Lazy Read Missing Model: Fetch {}x from the database that dont exist'.format(
        INSTANCES_TO_CREATE)

    CREATE_SINGLE_ROW = 'Create Model: Create a single row'
    CREATE_MULTI_ROW = 'Create Model: Create {}x rows at at time'.format(NUM_INSTANCES_TO_DESERIALIZE)
    CREATE_BULK_ROW = 'Create Model: Create {}x rows at at time'.format(INSTANCES_TO_CREATE)

    UPDATE_SINGLE_ROW = 'Update Model: Update a single row'
    UPDATE_MULTI_ROW = 'Update Model: Update {}x rows at a time'.format(NUM_INSTANCES_TO_DESERIALIZE)
    UPDATE_BULK_ROW = 'Update Model: Update {}x rows at a time'.format(INSTANCES_TO_CREATE)

    DELETE_SINGLE_ROW = 'Delete Model: Delete a single row'
    DELETE_MULTI_ROW = 'Delete Model: Delete {}x rows at a time'.format(NUM_INSTANCES_TO_DESERIALIZE)
    DELETE_BULK_ROW = 'Delete Model: Delete {}x rows at a time'.format(INSTANCES_TO_CREATE)


def benchmark_crud_models(klasses=None):
    if not klasses:
        klasses = model_classes()

    results = []
    tests = [
        _benchmark_READ_SINGLE_ROW,
        _benchmark_READ_MULTI_ROW,
        _benchmark_READ_BULK,
        _benchmark_READ_MISSING_BULK,

        _benchmark_CREATE_SINGLE_ROW,
        _benchmark_CREATE_MULTI_ROW,
        _benchmark_CREATE_BULK_ROW,

        _benchmark_UPDATE_SINGLE_ROW,
        _benchmark_UPDATE_MULTI_ROW,
        _benchmark_UPDATE_BULK_ROW,

        _benchmark_DELETE_SINGLE_ROW,
        _benchmark_DELETE_MULTI_ROW,
        _benchmark_DELETE_BULK_ROW,

        _benchmark_ASYNC_READ_SINGLE_ROW,
        _benchmark_ASYNC_READ_MULTI_ROW,
        _benchmark_ASYNC_READ_BULK,
        _benchmark_ASYNC_READ_MISSING_BULK,

        _benchmark_LAZY_READ_SINGLE_ROW,
        _benchmark_LAZY_READ_MULTI_ROW,
        _benchmark_LAZY_READ_BULK,
        _benchmark_LAZY_READ_MISSING_BULK,
    ]
    for test in tests:
        for klass in klasses:
            _logger.info((test.__name__, klass.__name__,))
            test_group, delta, iterations, row_count = test(klass)
            results.append(create_result(klass, test_group, delta, iterations, row_count))
            _logger.info(results[-1])

    return results


def _benchmark_READ_SINGLE_ROW(model_class):
    with create_row(model_class) as (row, key):
        def fn():
            model_class.get([key])

        seconds = benchmark_fn(fn, CRUD_ITERATIONS)
    return CrudTestGroups.READ_SINGLE_ROW, seconds, CRUD_ITERATIONS, 1


def _benchmark_READ_MULTI_ROW(model_class):
    with create_rows(model_class, NUM_INSTANCES_TO_DESERIALIZE) as (rows, keys):
        def fn():
            model_class.get(keys)

        seconds = benchmark_fn(fn, CRUD_ITERATIONS)
    return CrudTestGroups.READ_MULTI_ROW, seconds, CRUD_ITERATIONS, NUM_INSTANCES_TO_DESERIALIZE


def _benchmark_READ_BULK(model_class):
    with create_rows(model_class, INSTANCES_TO_CREATE) as (rows, keys):
        def fn():
            model_class.get(keys)

        seconds = benchmark_fn(fn, CRUD_ITERATIONS)
    return CrudTestGroups.READ_BULK, seconds, CRUD_ITERATIONS, INSTANCES_TO_CREATE


def _benchmark_READ_MISSING_BULK(model_class):
    with create_rows(model_class, INSTANCES_TO_CREATE) as (rows, keys):
        # Delete the rows to force a read-miss
        model_class.delete(rows)
        while len(filter(lambda x: x, model_class.get(keys))) > 0:
            time.sleep(0.1)

        def fn():
            model_class.get(keys)

        seconds = benchmark_fn(fn, CRUD_ITERATIONS)
    return CrudTestGroups.READ_MISSING_BULK, seconds, CRUD_ITERATIONS, INSTANCES_TO_CREATE


def _benchmark_ASYNC_READ_SINGLE_ROW(model_class):
    with create_row(model_class) as (row, key):
        if issubclass(model_class, ndb.Model):
            key = key.to_old_key()

        def fn():
            model_class.get_async([key])

        seconds = benchmark_fn(fn, CRUD_ITERATIONS)
    return CrudTestGroups.ASYNC_READ_SINGLE_ROW, seconds, CRUD_ITERATIONS, 1


def _benchmark_ASYNC_READ_MULTI_ROW(model_class):
    with create_rows(model_class, NUM_INSTANCES_TO_DESERIALIZE) as (rows, keys):
        if issubclass(model_class, ndb.Model):
            keys = [key.to_old_key() for key in keys]

        def fn():
            model_class.get_async(keys)

        seconds = benchmark_fn(fn, CRUD_ITERATIONS)
    return CrudTestGroups.ASYNC_READ_MULTI_ROW, seconds, CRUD_ITERATIONS, NUM_INSTANCES_TO_DESERIALIZE


def _benchmark_ASYNC_READ_BULK(model_class):
    with create_rows(model_class, INSTANCES_TO_CREATE) as (rows, keys):
        if issubclass(model_class, ndb.Model):
            keys = [key.to_old_key() for key in keys]

        def fn():
            model_class.get_async(keys)

        seconds = benchmark_fn(fn, CRUD_ITERATIONS)
    return CrudTestGroups.ASYNC_READ_BULK, seconds, CRUD_ITERATIONS, INSTANCES_TO_CREATE


def _benchmark_ASYNC_READ_MISSING_BULK(model_class):
    with create_rows(model_class, INSTANCES_TO_CREATE) as (rows, keys):
        # Delete the rows to force a read-miss
        model_class.delete(rows)
        while len(filter(lambda x: x, model_class.get(keys))) > 0:
            time.sleep(0.1)

        if issubclass(model_class, ndb.Model):
            keys = [key.to_old_key() for key in keys]

        def fn():
            model_class.get_async(keys)

        seconds = benchmark_fn(fn, CRUD_ITERATIONS)
    return CrudTestGroups.ASYNC_READ_MISSING_BULK, seconds, CRUD_ITERATIONS, INSTANCES_TO_CREATE


def _benchmark_LAZY_READ_SINGLE_ROW(model_class):
    with create_row(model_class) as (row, key):
        if issubclass(model_class, ndb.Model):
            key = key.to_old_key()

        def fn():
            model_class.get_lazy([key])

        seconds = benchmark_fn(fn, CRUD_ITERATIONS)
    return CrudTestGroups.LAZY_READ_SINGLE_ROW, seconds, CRUD_ITERATIONS, 1


def _benchmark_LAZY_READ_MULTI_ROW(model_class):
    with create_rows(model_class, NUM_INSTANCES_TO_DESERIALIZE) as (rows, keys):
        if issubclass(model_class, ndb.Model):
            keys = [key.to_old_key() for key in keys]

        def fn():
            model_class.get_lazy(keys)

        seconds = benchmark_fn(fn, CRUD_ITERATIONS)
    return CrudTestGroups.LAZY_READ_MULTI_ROW, seconds, CRUD_ITERATIONS, NUM_INSTANCES_TO_DESERIALIZE


def _benchmark_LAZY_READ_BULK(model_class):
    with create_rows(model_class, INSTANCES_TO_CREATE) as (rows, keys):
        if issubclass(model_class, ndb.Model):
            keys = [key.to_old_key() for key in keys]

        def fn():
            model_class.get_lazy(keys)

        seconds = benchmark_fn(fn, CRUD_ITERATIONS)
    return CrudTestGroups.LAZY_READ_BULK, seconds, CRUD_ITERATIONS, INSTANCES_TO_CREATE


def _benchmark_LAZY_READ_MISSING_BULK(model_class):
    with create_rows(model_class, INSTANCES_TO_CREATE) as (rows, keys):
        # Delete the rows to force a read-miss
        model_class.delete(rows)
        while len(filter(lambda x: x, model_class.get(keys))) > 0:
            time.sleep(0.1)

        if issubclass(model_class, ndb.Model):
            keys = [key.to_old_key() for key in keys]

        def fn():
            model_class.get_lazy(keys)

        seconds = benchmark_fn(fn, CRUD_ITERATIONS)
    return CrudTestGroups.LAZY_READ_MISSING_BULK, seconds, CRUD_ITERATIONS, INSTANCES_TO_CREATE


def _benchmark_CREATE_SINGLE_ROW(model_class):
    rows = []

    def fn():
        row = model_class()
        for property in row._properties.keys():
            setattr(row, property, str(uuid.uuid4()))
        model_class.put([row])
        rows.append(row)

    seconds = benchmark_fn(fn, CRUD_ITERATIONS)

    # Cleanup after the test
    model_class.delete(rows)

    return CrudTestGroups.CREATE_SINGLE_ROW, seconds, CRUD_ITERATIONS, 1


def _benchmark_CREATE_MULTI_ROW(model_class):
    rows = []

    def fn():
        local_rows = []
        for _ in range(NUM_INSTANCES_TO_DESERIALIZE):
            row = model_class()
            for property in row._properties.keys():
                setattr(row, property, str(uuid.uuid4()))
            local_rows.append(row)
        model_class.put(local_rows)
        rows.extend(local_rows)

    seconds = benchmark_fn(fn, CRUD_ITERATIONS)

    # Cleanup after the test
    model_class.delete(rows)

    return CrudTestGroups.CREATE_MULTI_ROW, seconds, CRUD_ITERATIONS, NUM_INSTANCES_TO_DESERIALIZE


def _benchmark_CREATE_BULK_ROW(model_class):
    rows = []

    def fn():
        local_rows = []
        for _ in range(CRUD_ITERATIONS):
            row = model_class()
            for property in row._properties.keys():
                setattr(row, property, str(uuid.uuid4()))
            local_rows.append(row)
        model_class.put(local_rows)
        rows.extend(local_rows)

    seconds = benchmark_fn(fn, CRUD_ITERATIONS)

    # Cleanup after the test
    model_class.delete(rows)

    return CrudTestGroups.CREATE_BULK_ROW, seconds, CRUD_ITERATIONS, CRUD_ITERATIONS


def _benchmark_UPDATE_SINGLE_ROW(model_class):
    with create_row(model_class) as (row, key):
        def fn():
            for property in row._properties.keys():
                setattr(row, property, str(uuid.uuid4()))
            model_class.put([row])

        seconds = benchmark_fn(fn, CRUD_ITERATIONS)
    return CrudTestGroups.UPDATE_SINGLE_ROW, seconds, CRUD_ITERATIONS, 1


def _benchmark_UPDATE_MULTI_ROW(model_class):
    with create_rows(model_class, NUM_INSTANCES_TO_DESERIALIZE) as (rows, keys):
        def fn():
            for row in rows:
                for property in row._properties.keys():
                    setattr(row, property, str(uuid.uuid4()))
            model_class.put(rows)

        seconds = benchmark_fn(fn, CRUD_ITERATIONS)
    return CrudTestGroups.UPDATE_MULTI_ROW, seconds, CRUD_ITERATIONS, NUM_INSTANCES_TO_DESERIALIZE


def _benchmark_UPDATE_BULK_ROW(model_class):
    with create_rows(model_class, CRUD_ITERATIONS) as (rows, keys):
        def fn():
            for row in rows:
                for property in row._properties.keys():
                    setattr(row, property, str(uuid.uuid4()))
            model_class.put(rows)

        seconds = benchmark_fn(fn, CRUD_ITERATIONS)
    return CrudTestGroups.UPDATE_BULK_ROW, seconds, CRUD_ITERATIONS, CRUD_ITERATIONS


def _benchmark_DELETE_SINGLE_ROW(model_class):
    with create_rows(model_class, CRUD_ITERATIONS) as (rows, keys):
        def fn():
            row = rows.pop(0)
            model_class.delete([row])

        seconds = benchmark_fn(fn, CRUD_ITERATIONS)
    return CrudTestGroups.DELETE_SINGLE_ROW, seconds, CRUD_ITERATIONS, CRUD_ITERATIONS


def _benchmark_DELETE_MULTI_ROW(model_class):
    with create_rows(model_class, NUM_INSTANCES_TO_DESERIALIZE * CRUD_ITERATIONS) as (rows, keys):
        def fn():
            rows_slice = [rows.pop(0) for _ in range(NUM_INSTANCES_TO_DESERIALIZE)]
            model_class.delete(rows_slice)

        seconds = benchmark_fn(fn, CRUD_ITERATIONS)
    return CrudTestGroups.DELETE_MULTI_ROW, seconds, CRUD_ITERATIONS, NUM_INSTANCES_TO_DESERIALIZE


def _benchmark_DELETE_BULK_ROW(model_class):
    with create_rows(model_class, CRUD_ITERATIONS * CRUD_ITERATIONS) as (rows, keys):
        def fn():
            rows_slice = [rows.pop(0) for _ in range(CRUD_ITERATIONS)]
            model_class.delete(rows_slice)

        seconds = benchmark_fn(fn, CRUD_ITERATIONS)
    return CrudTestGroups.DELETE_BULK_ROW, seconds, CRUD_ITERATIONS, CRUD_ITERATIONS
