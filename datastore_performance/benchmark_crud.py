from __future__ import absolute_import

import time

import enum

from datastore_performance.constants import INSTANCES_TO_CREATE, SERIALIZATION_ITERATIONS
from datastore_performance.data_generator import create_row, create_rows


@enum.unique
class CrudTestGroups(enum.Enum):
    READ_SINGLE_ROW = 'read: fetch a single row'
    READ_MULTI_ROW = 'read: fetch 10x rows'
    READ_BULK = 'read: read {}x rows from the database at at time'.format(INSTANCES_TO_CREATE)

    CREATE_SINGLE_ROW = 'create: create a single row'
    CREATE_MULTI_ROW = 'create: create 10x rows at at time'

    UPDATE_SINGLE_ROW = 'update: update a single row'
    UPDATE_MULTI_ROW = 'update: update 10x rows at a time'
    UPDATE_BULK_ROW = 'update: update {}x rows at a time'.format(INSTANCES_TO_CREATE)

    DELETE_SINGLE_ROW = 'delete: delete a single row'
    DELETE_MULTI_ROW = 'delete: delete 10x rows at a time'
    DELETE_BULK_ROW = 'delete: delete {}x rows at a time'.format(INSTANCES_TO_CREATE)


def _benchmark_READ_SINGLE_ROW(model_class):
    with create_row(model_class) as row:
        start = time.time()
        for _ in range(SERIALIZATION_ITERATIONS):
            model_class.get(row.key())
        end = time.time()
    return CrudTestGroups.READ_SINGLE_ROW, float(end - start)


def _benchmark_READ_MULTI_ROW(model_classs):
    with create_rows(model_classs, 10) as rows:
        keys = map(lambda x: x.key(), rows)
        start = time.time()
        for _ in range(SERIALIZATION_ITERATIONS):
            model_classs.get(keys)
        end = time.time()
    return CrudTestGroups.READ_MULTI_ROW, float(end - start)


def _benchmark_READ_BULK(model_classs):
    with create_rows(model_classs, INSTANCES_TO_CREATE) as rows:
        keys = map(lambda x: x.key(), rows)
        start = time.time()
        for _ in range(SERIALIZATION_ITERATIONS):
            model_classs.get(keys)
        end = time.time()
    return CrudTestGroups.READ_BULK, float(end - start)


def bench(response, model_class, keys):
    for i in range(ITERATIONS):
        total = 0
        start = time.time()
        entities = model_class.get(keys)
        end = time.time()
        output(response, '  %s.get %d entities in %f seconds (total: %d)' % (
            model_class.__name__, len(entities), (end - start), total))

    if issubclass(model_class, ndb.Model):
        keys = [k.to_old_key() for k in keys]

    for i in range(ITERATIONS):
        start = time.time()
        rpc = datastore.GetAsync(keys)
        entities = rpc.get_result()
        end = time.time()

        if DUMP_ENTITIES and i == 0:
            response.write('\n')
            response.write('## ENTITY CONTENTS:\n')
            response.write(repr(entities))
            response.write('\n\n')

            for i, entity in enumerate(entities):
                response.write('  %d: %d keys %d serialized bytes\n' % (i, len(entity), entity.ToPb().ByteSize()))

        output(response, '  datastore.GetAsync %d entities in %f seconds (total %d)' % (
            len(entities), (end - start), total))

    for i in range(ITERATIONS):
        start = time.time()
        entities = datastore_lazy.get(keys)
        end = time.time()

        output(response, '  datastore_lazy.get %d entities in %f seconds (total %d)' % (
            len(entities), (end - start), total))


def find_keys_and_bench(response, model_class):
    # Query for models
    keys = model_class.keys(NUM_INSTANCES_TO_DESERIALIZE)

    response.write('## ENTITY KEYS:\n')
    for key in keys:
        if isinstance(key, db.Key):
            s = str(key)
        else:
            s = key.urlsafe()
        response.write(s + '\n')

    bench(response, model_class, keys)
