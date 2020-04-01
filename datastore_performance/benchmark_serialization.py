from __future__ import absolute_import

import enum
from google.appengine.api import datastore
from google.appengine.datastore import entity_pb

from datastore_performance import datastore_lazy
from datastore_performance.constants import DB_MODEL_CLASSES, \
    SERIALIZATION_ITERATIONS, create_result, create_row, benchmark_fn


@enum.unique
class SerializationTestGroups(enum.Enum):
    MODEL_TO_PROTOBUF_STRING = 'serialize: model -> db.Entity -> entity_pb.EntityProto -> Protobuf string'
    ENTITY_TO_PROTOBUF_STRING = 'serialize: db.Entity -> entity_pb.EntityProto -> Protobuf string'
    ENTITY_PROTO_TO_PROTOBUF_STRING = 'serialize: entity_pb.EntityProto -> Protobuf string'

    PROTOBUF_STRING_TO_MODEL = 'deserialize: Protobuf string --> model --> entity_pb.EntityProto --< db.Entity'
    PROTOBUF_STRING_TO_ENTITY = 'deserialize: Protobuf string --> db.Entity <- entity_pb.EntityProto'
    PROTOBUF_STRING_TO_ENTITY_PROTO = 'deserialize: Protobuf string --> entity_pb.EntityProto'
    PROTOBUF_STRING_TO_ENTITY_PROTO_WITH_REUSE = 'deserialize: Protobuf string --> entity_pb.EntityProto with protobuf reuse'

    SINGLE_PROPERTY_ACCESS_TIMES_PROTOBUF_TO_MODEL = '1x property access time, deserialize: entity_pb.EntityProto <- Protobuf string with protobuf reuse'
    MULTI_PROPERTY_ACCESS_TIMES_PROTOBUF_TO_MODEL = '10x property access time, deserialize: entity_pb.EntityProto <- Protobuf string with protobuf reuse'

    SINGLE_LAZY_PROPERTY_ACCESS_TIMES_PROTOBUF_TO_MODEL = '1x lazy property access time, deserialize: entity_pb.EntityProto <- Protobuf string with protobuf reuse'
    MULTI_LAZY_PROPERTY_ACCESS_TIMES_PROTOBUF_TO_MODEL = '10x lazy property access time, deserialize: entity_pb.EntityProto <- Protobuf string with protobuf reuse'

    PROTOBUF_PROPERTY_SIZE = 'pure python access to protobuf->property_size'


def benchmark_serialization_models():
    results = []
    for klass in DB_MODEL_CLASSES:
        results.extend(_benchmark_serialization(klass))
    return results


def _benchmark_serialization(model_class):
    # How data gets from a db.Model subclass to bytes:
    # 1. db.Model is converted to a datastore.Entity
    # 2. datastore.Entity is converted to a protocol buffer object: EntityProto
    # 3. EntityProto is serialized

    results = []

    tests = [
        _benchmark_MODEL_TO_PROTOBUF_STRING,
        _benchmark_ENTITY_TO_PROTOBUF_STRING,
        _benchmark_ENTITY_PROTO_TO_PROTOBUF_STRING,
        _benchmark_PROTOBUF_STRING_TO_MODEL,
        _benchmark_PROTOBUF_STRING_TO_ENTITY,
        _benchmark_PROTOBUF_STRING_TO_ENTITY_PROTO,
        _benchmark_PROTOBUF_STRING_TO_ENTITY_PROTO_WITH_REUSE,
        _benchmark_SINGLE_PROPERTY_ACCESS_TIMES_PROTOBUF_TO_MODEL,
        _benchmark_MULTI_PROPERTY_ACCESS_TIMES_PROTOBUF_TO_MODEL,
        _benchmark_SINGLE_LAZY_PROPERTY_ACCESS_TIMES_PROTOBUF_TO_MODEL,
        _benchmark_MULTI_LAZY_PROPERTY_ACCESS_TIMES_PROTOBUF_TO_MODEL,
        _benchmark_PROTOBUF_PROPERTY_SIZE,
    ]
    for test in tests:
        test_group, delta, iterations = test(model_class)
        results.append(create_result(model_class, test_group, delta, iterations))

    return results


def _benchmark_MODEL_TO_PROTOBUF_STRING(model_class):
    with create_row(model_class) as (row, key):
        def fn():
            entity = row._populate_entity(datastore.Entity)
            entity_proto = entity.ToPb()
            entity_proto.SerializeToString()

        seconds = benchmark_fn(fn, SERIALIZATION_ITERATIONS)
        return SerializationTestGroups.MODEL_TO_PROTOBUF_STRING, seconds, SERIALIZATION_ITERATIONS


def _benchmark_ENTITY_TO_PROTOBUF_STRING(model_class):
    with create_row(model_class) as (row, key):
        entity = row._populate_entity(datastore.Entity)

        def fn():
            entity_proto = entity.ToPb()
            entity_proto.SerializeToString()

        seconds = benchmark_fn(fn, SERIALIZATION_ITERATIONS)
        return SerializationTestGroups.ENTITY_TO_PROTOBUF_STRING, seconds, SERIALIZATION_ITERATIONS


def _benchmark_ENTITY_PROTO_TO_PROTOBUF_STRING(model_class):
    with create_row(model_class) as (row, key):
        entity = row._populate_entity(datastore.Entity)
        entity_proto = entity.ToPb()

        def fn():
            entity_proto.SerializeToString()

        seconds = benchmark_fn(fn, SERIALIZATION_ITERATIONS)
        return SerializationTestGroups.ENTITY_PROTO_TO_PROTOBUF_STRING, seconds, SERIALIZATION_ITERATIONS


def _benchmark_PROTOBUF_STRING_TO_MODEL(model_class):
    with create_row(model_class) as (row, key):
        entity = row._populate_entity(datastore.Entity)
        entity_proto = entity.ToPb()
        serialized = entity_proto.SerializeToString()

        def fn():
            entity_proto = entity_pb.EntityProto(serialized)
            entity = datastore.Entity.FromPb(entity_proto)
            model_class.from_entity(entity)

        seconds = benchmark_fn(fn, SERIALIZATION_ITERATIONS)
        return SerializationTestGroups.PROTOBUF_STRING_TO_MODEL, seconds, SERIALIZATION_ITERATIONS


def _benchmark_PROTOBUF_STRING_TO_ENTITY(model_class):
    with create_row(model_class) as (row, key):
        entity = row._populate_entity(datastore.Entity)
        entity_proto = entity.ToPb()
        serialized = entity_proto.SerializeToString()

        def fn():
            entity_proto = entity_pb.EntityProto(serialized)
            datastore.Entity.FromPb(entity_proto)

        seconds = benchmark_fn(fn, SERIALIZATION_ITERATIONS)
        return SerializationTestGroups.PROTOBUF_STRING_TO_ENTITY, seconds, SERIALIZATION_ITERATIONS


def _benchmark_PROTOBUF_STRING_TO_ENTITY_PROTO(model_class):
    with create_row(model_class) as (row, key):
        entity = row._populate_entity(datastore.Entity)
        entity_proto = entity.ToPb()
        serialized = entity_proto.SerializeToString()

        def fn():
            entity_proto = entity_pb.EntityProto(serialized)
            datastore.Entity.FromPb(entity_proto)

        seconds = benchmark_fn(fn, SERIALIZATION_ITERATIONS)
        return SerializationTestGroups.PROTOBUF_STRING_TO_ENTITY_PROTO, seconds, SERIALIZATION_ITERATIONS


def _benchmark_PROTOBUF_STRING_TO_ENTITY_PROTO_WITH_REUSE(model_class):
    with create_row(model_class) as (row, key):
        entity = row._populate_entity(datastore.Entity)
        entity_proto = entity.ToPb()
        serialized = entity_proto.SerializeToString()

        def fn():
            entity_proto.Clear()
            entity_proto.MergeFromString(serialized)

        seconds = benchmark_fn(fn, SERIALIZATION_ITERATIONS)
        return SerializationTestGroups.PROTOBUF_STRING_TO_ENTITY_PROTO_WITH_REUSE, seconds, SERIALIZATION_ITERATIONS


def _benchmark_SINGLE_PROPERTY_ACCESS_TIMES_PROTOBUF_TO_MODEL(model_class):
    with create_row(model_class) as (row, key):
        entity = row._populate_entity(datastore.Entity)
        entity_proto = entity.ToPb()
        serialized = entity_proto.SerializeToString()

        def fn():
            entity_proto = entity_pb.EntityProto(serialized)
            entity = datastore.Entity.FromPb(entity_proto)
            deserialized = model_class.from_entity(entity)
            len(deserialized.prop_0)

        seconds = benchmark_fn(fn, SERIALIZATION_ITERATIONS)
        return SerializationTestGroups.SINGLE_PROPERTY_ACCESS_TIMES_PROTOBUF_TO_MODEL, seconds, SERIALIZATION_ITERATIONS


def _benchmark_MULTI_PROPERTY_ACCESS_TIMES_PROTOBUF_TO_MODEL(model_class):
    with create_row(model_class) as (row, key):
        entity = row._populate_entity(datastore.Entity)
        entity_proto = entity.ToPb()
        serialized = entity_proto.SerializeToString()

        def fn():
            entity_proto = entity_pb.EntityProto(serialized)
            entity = datastore.Entity.FromPb(entity_proto)
            deserialized = model_class.from_entity(entity)
            len(deserialized.prop_0)
            len(deserialized.prop_1)
            len(deserialized.prop_2)
            len(deserialized.prop_3)
            len(deserialized.prop_4)
            len(deserialized.prop_5)
            len(deserialized.prop_6)
            len(deserialized.prop_7)
            len(deserialized.prop_8)
            len(deserialized.prop_9)

        seconds = benchmark_fn(fn, SERIALIZATION_ITERATIONS)
        return SerializationTestGroups.MULTI_PROPERTY_ACCESS_TIMES_PROTOBUF_TO_MODEL, seconds, SERIALIZATION_ITERATIONS


def _benchmark_SINGLE_LAZY_PROPERTY_ACCESS_TIMES_PROTOBUF_TO_MODEL(model_class):
    with create_row(model_class) as (row, key):
        entity = row._populate_entity(datastore.Entity)
        entity_proto = entity.ToPb()
        serialized = entity_proto.SerializeToString()

        def fn():
            entity_proto = entity_pb.EntityProto(serialized)
            deserialized = datastore_lazy.LazyEntity(entity_proto)
            len(deserialized.prop_0)

        seconds = benchmark_fn(fn, SERIALIZATION_ITERATIONS)
        return SerializationTestGroups.SINGLE_LAZY_PROPERTY_ACCESS_TIMES_PROTOBUF_TO_MODEL, seconds, SERIALIZATION_ITERATIONS


def _benchmark_MULTI_LAZY_PROPERTY_ACCESS_TIMES_PROTOBUF_TO_MODEL(model_class):
    with create_row(model_class) as (row, key):
        entity = row._populate_entity(datastore.Entity)
        entity_proto = entity.ToPb()
        serialized = entity_proto.SerializeToString()

        def fn():
            entity_proto = entity_pb.EntityProto(serialized)
            deserialized = datastore_lazy.LazyEntity(entity_proto)
            len(deserialized.prop_0)
            len(deserialized.prop_1)
            len(deserialized.prop_2)
            len(deserialized.prop_3)
            len(deserialized.prop_4)
            len(deserialized.prop_5)
            len(deserialized.prop_6)
            len(deserialized.prop_7)
            len(deserialized.prop_8)
            len(deserialized.prop_9)

        seconds = benchmark_fn(fn, SERIALIZATION_ITERATIONS)
        return SerializationTestGroups.MULTI_LAZY_PROPERTY_ACCESS_TIMES_PROTOBUF_TO_MODEL, seconds, SERIALIZATION_ITERATIONS


def _benchmark_PROTOBUF_PROPERTY_SIZE(model_class):
    with create_row(model_class) as (row, key):
        entity = row._populate_entity(datastore.Entity)
        entity_proto = entity.ToPb()
        serialized = entity_proto.SerializeToString()

        def fn():
            entity_proto = entity_pb.EntityProto(serialized)
            entity_proto.property_size()

        seconds = benchmark_fn(fn, SERIALIZATION_ITERATIONS)
        return SerializationTestGroups.PROTOBUF_PROPERTY_SIZE, seconds, SERIALIZATION_ITERATIONS
