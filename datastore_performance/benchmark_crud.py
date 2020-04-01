from __future__ import absolute_import

import time
import uuid

import enum
from google.appengine.api import datastore

from datastore_performance import datastore_lazy
from datastore_performance.constants import INSTANCES_TO_CREATE, SERIALIZATION_ITERATIONS, NUM_INSTANCES_TO_DESERIALIZE, \
    DB_MODEL_CLASSES, create_result, create_row, create_rows, benchmark_fn


@enum.unique
class CrudTestGroups(enum.Enum):
    READ_SINGLE_ROW = 'read: fetch a single row'
    READ_MULTI_ROW = 'read: fetch {}x rows'.format(NUM_INSTANCES_TO_DESERIALIZE)
    READ_BULK = 'read: read {}x rows from the database at at time'.format(INSTANCES_TO_CREATE)
    READ_MISSING_BULK = 'read missing: read {}x from the database that dont exist'.format(INSTANCES_TO_CREATE)

    ASYNC_READ_SINGLE_ROW = 'async read: fetch a single row'
    ASYNC_READ_MULTI_ROW = 'async read: fetch {}x rows'.format(NUM_INSTANCES_TO_DESERIALIZE)
    ASYNC_READ_BULK = 'async read: read {}x rows from the database at at time'.format(INSTANCES_TO_CREATE)
    ASYNC_READ_MISSING_BULK = 'async read missing: read {}x from the database that dont exist'.format(
        INSTANCES_TO_CREATE)

    LAZY_READ_SINGLE_ROW = 'lazy read: fetch a single row'
    LAZY_READ_MULTI_ROW = 'lazy read: fetch {}x rows'.format(NUM_INSTANCES_TO_DESERIALIZE)
    LAZY_READ_BULK = 'lazy read: read {}x rows from the database at at time'.format(INSTANCES_TO_CREATE)
    LAZY_READ_MISSING_BULK = 'lazy read missing: read {}x from the database that dont exist'.format(INSTANCES_TO_CREATE)

    CREATE_SINGLE_ROW = 'create: create a single row'
    CREATE_MULTI_ROW = 'create: create {}x rows at at time'.format(NUM_INSTANCES_TO_DESERIALIZE)

    UPDATE_SINGLE_ROW = 'update: update a single row'
    UPDATE_MULTI_ROW = 'update: update {}x rows at a time'.format(NUM_INSTANCES_TO_DESERIALIZE)
    UPDATE_BULK_ROW = 'update: update {}x rows at a time'.format(INSTANCES_TO_CREATE)

    DELETE_SINGLE_ROW = 'delete: delete a single row'
    DELETE_MULTI_ROW = 'delete: delete {}x rows at a time'.format(NUM_INSTANCES_TO_DESERIALIZE)
    DELETE_BULK_ROW = 'delete: delete {}x rows at a time'.format(INSTANCES_TO_CREATE)


def benchmark_crud():
    results = []
    for klass in DB_MODEL_CLASSES:
        results.extend(_benchmark_crud(klass))
    return results


def _benchmark_crud(model_class):
    # How data gets from a db.Model subclass to bytes:
    # 1. db.Model is converted to a datastore.Entity
    # 2. datastore.Entity is converted to a protocol buffer object: EntityProto
    # 3. EntityProto is serialized

    results = []

    tests = [
        # _benchmark_READ_SINGLE_ROW,
        # _benchmark_READ_MULTI_ROW,
        # _benchmark_READ_BULK,
        # _benchmark_READ_MISSING_BULK,
        # _benchmark_ASYNC_READ_SINGLE_ROW,
        # _benchmark_ASYNC_READ_MULTI_ROW,
        # _benchmark_ASYNC_READ_BULK,
        # _benchmark_ASYNC_READ_MISSING_BULK,
        # _benchmark_LAZY_READ_SINGLE_ROW,
        # _benchmark_LAZY_READ_MULTI_ROW,
        # _benchmark_LAZY_READ_BULK,
        # _benchmark_LAZY_READ_MISSING_BULK,
        # _benchmark_CREATE_SINGLE_ROW,
        # _benchmark_CREATE_MULTI_ROW,
        # _benchmark_UPDATE_SINGLE_ROW,
        # _benchmark_UPDATE_MULTI_ROW,
        # _benchmark_UPDATE_BULK_ROW,
        # _benchmark_DELETE_SINGLE_ROW,
        # _benchmark_DELETE_MULTI_ROW,
        # _benchmark_DELETE_BULK_ROW,
    ]
    for test in tests:
        test_group, delta, iterations = test(model_class)
        results.append(create_result(model_class, test_group, delta, iterations))

    return results


def _benchmark_READ_SINGLE_ROW(model_class):
    with create_row(model_class) as (row, key):
        def fn():
            model_class.get(key)

        seconds = benchmark_fn(fn, SERIALIZATION_ITERATIONS)
    return CrudTestGroups.READ_SINGLE_ROW, seconds, SERIALIZATION_ITERATIONS


def _benchmark_READ_MULTI_ROW(model_classs):
    with create_rows(model_classs, NUM_INSTANCES_TO_DESERIALIZE) as (rows, keys):
        def fn():
            model_classs.get(keys)

        seconds = benchmark_fn(fn, SERIALIZATION_ITERATIONS)
    return CrudTestGroups.READ_MULTI_ROW, seconds, SERIALIZATION_ITERATIONS


def _benchmark_READ_BULK(model_classs):
    with create_rows(model_classs, INSTANCES_TO_CREATE) as (rows, keys):
        def fn():
            model_classs.get(keys)

        seconds = benchmark_fn(fn, SERIALIZATION_ITERATIONS)
    return CrudTestGroups.READ_BULK, seconds, SERIALIZATION_ITERATIONS


def _benchmark_READ_MISSING_BULK(model_classs):
    with create_rows(model_classs, INSTANCES_TO_CREATE) as (rows, keys):
        # Delete the rows to force a read-miss
        model_classs.delete(keys)
        while len(filter(lambda x: x, model_classs.get(keys))) > 0:
            time.sleep(0.5)

        def fn():
            model_classs.get(keys)

        seconds = benchmark_fn(fn, SERIALIZATION_ITERATIONS)
    return CrudTestGroups.READ_MISSING_BULK, seconds, SERIALIZATION_ITERATIONS


def _benchmark_ASYNC_READ_SINGLE_ROW(model_class):
    with create_row(model_class) as (row, key):
        def fn():
            rpc = datastore.GetAsync([key])
            rpc.get_result()

        seconds = benchmark_fn(fn, SERIALIZATION_ITERATIONS)
    return CrudTestGroups.ASYNC_READ_SINGLE_ROW, seconds, SERIALIZATION_ITERATIONS


def _benchmark_ASYNC_READ_MULTI_ROW(model_classs):
    with create_rows(model_classs, NUM_INSTANCES_TO_DESERIALIZE) as (rows, keys):
        def fn():
            rpc = datastore.GetAsync(keys)
            rpc.get_result()

        seconds = benchmark_fn(fn, SERIALIZATION_ITERATIONS)
    return CrudTestGroups.ASYNC_READ_MULTI_ROW, seconds, SERIALIZATION_ITERATIONS


def _benchmark_ASYNC_READ_BULK(model_classs):
    with create_rows(model_classs, INSTANCES_TO_CREATE) as (rows, keys):
        def fn():
            rpc = datastore.GetAsync(keys)
            rpc.get_result()

        seconds = benchmark_fn(fn, SERIALIZATION_ITERATIONS)
    return CrudTestGroups.ASYNC_READ_BULK, seconds, SERIALIZATION_ITERATIONS


def _benchmark_ASYNC_READ_MISSING_BULK(model_classs):
    with create_rows(model_classs, INSTANCES_TO_CREATE) as (rows, keys):
        # Delete the rows to force a read-miss
        model_classs.delete(keys)
        while len(filter(lambda x: x, model_classs.get(keys))) > 0:
            time.sleep(0.5)

        def fn():
            rpc = datastore.GetAsync(keys)
            rpc.get_result()

        seconds = benchmark_fn(fn, SERIALIZATION_ITERATIONS)
    return CrudTestGroups.ASYNC_READ_MISSING_BULK, seconds, SERIALIZATION_ITERATIONS


def _benchmark_LAZY_READ_SINGLE_ROW(model_class):
    with create_row(model_class) as (row, key):
        def fn():
            datastore_lazy.get([key])

        seconds = benchmark_fn(fn, SERIALIZATION_ITERATIONS)
    return CrudTestGroups.LAZY_READ_SINGLE_ROW, seconds, SERIALIZATION_ITERATIONS


def _benchmark_LAZY_READ_MULTI_ROW(model_classs):
    with create_rows(model_classs, NUM_INSTANCES_TO_DESERIALIZE) as (rows, keys):
        def fn():
            datastore_lazy.get(keys)

        seconds = benchmark_fn(fn, SERIALIZATION_ITERATIONS)
    return CrudTestGroups.LAZY_READ_MULTI_ROW, seconds, SERIALIZATION_ITERATIONS


def _benchmark_LAZY_READ_BULK(model_classs):
    with create_rows(model_classs, INSTANCES_TO_CREATE) as (rows, keys):
        def fn():
            datastore_lazy.get(keys)

        seconds = benchmark_fn(fn, SERIALIZATION_ITERATIONS)
    return CrudTestGroups.LAZY_READ_BULK, seconds, SERIALIZATION_ITERATIONS


def _benchmark_LAZY_READ_MISSING_BULK(model_classs):
    with create_rows(model_classs, INSTANCES_TO_CREATE) as (rows, keys):
        # Delete the rows to force a read-miss
        model_classs.delete(keys)
        while len(filter(lambda x: x, model_classs.get(keys))) > 0:
            time.sleep(0.5)

        def fn():
            datastore_lazy.get(keys)

        seconds = benchmark_fn(fn, SERIALIZATION_ITERATIONS)
    return CrudTestGroups.LAZY_READ_MISSING_BULK, seconds, SERIALIZATION_ITERATIONS


def _benchmark_CREATE_SINGLE_ROW(model_class):
    rows = []

    def fn():
        row = model_class()
        for property in row._properties.keys():
            setattr(row, property, str(uuid.uuid4()))
        model_class.put(row)
        rows.append(row)

    seconds = benchmark_fn(fn, SERIALIZATION_ITERATIONS)

    # Cleanup after the test
    model_class.delete(rows)

    return CrudTestGroups.CREATE_SINGLE_ROW, seconds, SERIALIZATION_ITERATIONS


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

    seconds = benchmark_fn(fn, SERIALIZATION_ITERATIONS)

    # Cleanup after the test
    model_class.delete(rows)

    return CrudTestGroups.CREATE_MULTI_ROW, seconds, SERIALIZATION_ITERATIONS


def _benchmark_UPDATE_SINGLE_ROW(model_class):
    with create_row(model_class) as (row, key):
        def fn():
            for property in row._properties.keys():
                setattr(row, property, str(uuid.uuid4()))
            model_class.put(row)

        seconds = benchmark_fn(fn, SERIALIZATION_ITERATIONS)
    return CrudTestGroups.UPDATE_SINGLE_ROW, seconds, SERIALIZATION_ITERATIONS


def _benchmark_UPDATE_MULTI_ROW(model_class):
    with create_rows(model_class, NUM_INSTANCES_TO_DESERIALIZE) as (rows, keys):
        def fn():
            for row in rows:
                for property in row._properties.keys():
                    setattr(row, property, str(uuid.uuid4()))
            model_class.put(rows)

        seconds = benchmark_fn(fn, SERIALIZATION_ITERATIONS)
    return CrudTestGroups.UPDATE_MULTI_ROW, seconds, SERIALIZATION_ITERATIONS


def _benchmark_UPDATE_BULK_ROW(model_class):
    with create_rows(model_class, SERIALIZATION_ITERATIONS) as (rows, keys):
        def fn():
            for row in rows:
                for property in row._properties.keys():
                    setattr(row, property, str(uuid.uuid4()))
            model_class.put(rows)

        seconds = benchmark_fn(fn, SERIALIZATION_ITERATIONS)
    return CrudTestGroups.UPDATE_BULK_ROW, seconds, SERIALIZATION_ITERATIONS


def _benchmark_DELETE_SINGLE_ROW(model_class):
    with create_rows(model_class, SERIALIZATION_ITERATIONS) as (rows, keys):
        def fn():
            row = rows.pop(0)
            model_class.delete(row)

        seconds = benchmark_fn(fn, SERIALIZATION_ITERATIONS)
    return CrudTestGroups.DELETE_SINGLE_ROW, seconds, SERIALIZATION_ITERATIONS


def _benchmark_DELETE_MULTI_ROW(model_class):
    with create_rows(model_class, NUM_INSTANCES_TO_DESERIALIZE * SERIALIZATION_ITERATIONS) as (rows, keys):
        def fn():
            rows_slice = [rows.pop(0) for _ in range(NUM_INSTANCES_TO_DESERIALIZE)]
            model_class.delete(rows_slice)

        seconds = benchmark_fn(fn, SERIALIZATION_ITERATIONS)
    return CrudTestGroups.DELETE_MULTI_ROW, seconds, SERIALIZATION_ITERATIONS


def _benchmark_DELETE_BULK_ROW(model_class):
    with create_rows(model_class, SERIALIZATION_ITERATIONS * SERIALIZATION_ITERATIONS) as (rows, keys):
        def fn():
            rows_slice = [rows.pop(0) for _ in range(SERIALIZATION_ITERATIONS)]
            model_class.delete(rows_slice)

        seconds = benchmark_fn(fn, SERIALIZATION_ITERATIONS)
    return CrudTestGroups.DELETE_BULK_ROW, seconds, SERIALIZATION_ITERATIONS
