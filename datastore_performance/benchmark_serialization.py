from __future__ import absolute_import

import enum
from google.appengine.api import datastore
from google.appengine.datastore import entity_pb

from datastore_performance import datastore_lazy
from datastore_performance.constants import create_result, create_row, benchmark_fn, \
    model_classes

SERIALIZATION_ITERATIONS = 1000


@enum.unique
class SerializationTestGroups(enum.Enum):
    MODEL_TO_PROTOBUF_STRING = 'serialize Model: model --> ... --> ... --> Protobuf binary (3-4x steps)'
    ENTITY_TO_PROTOBUF_STRING = 'serialize db.Entity: db.Entity --> ... --> Protobuf binary (2-3x steps)'
    ENTITY_PROTO_TO_PROTOBUF_STRING = 'serialize Protobuf data: entity_pb.EntityProto --> Protobuf binary (1x step)'

    PROTOBUF_STRING_TO_MODEL = 'deserialize into Model: Protobuf binary --> ... --> Model (3-4x steps)'
    PROTOBUF_STRING_TO_ENTITY = 'deserialize into db.Entity: Protobuf binary --> ... --> db.Entity (2-3x steps)'
    PROTOBUF_STRING_TO_ENTITY_PROTO = 'deserialize into Protobuf data: Protobuf binary --> entity_pb.EntityProto (1x step)'
    # PROTOBUF_STRING_TO_ENTITY_PROTO_WITH_REUSE = 'deserialize: Protobuf binary --> entity_pb.EntityProto with protobuf reuse'

    SINGLE_PROPERTY_ACCESS_TIMES_PROTOBUF_TO_MODEL = 'deserialize and read 1x property from the model: deserialize into Model w/ reading properties from the model'
    MULTI_PROPERTY_ACCESS_TIMES_PROTOBUF_TO_MODEL = 'deserialize and read 10x properties from the model: deserialize into Model w/ reading properties from the model'

    SINGLE_LAZY_PROPERTY_ACCESS_TIMES_PROTOBUF_TO_MODEL = 'deserialize and lazily read 1x property from the model: deserialize into Model w/ reading properties from the model'
    MULTI_LAZY_PROPERTY_ACCESS_TIMES_PROTOBUF_TO_MODEL = 'deserialize and lazily read 10x properties from the model: deserialize into Model w/ reading properties from the model'

    # PROTOBUF_PROPERTY_SIZE = 'pure python access to protobuf->property_size'


def benchmark_serialization_models(klasses=None):
    if not klasses:
        klasses = model_classes()

    #
    # How data gets from a db.Model subclass to bytes:
    #
    # 1. db.Model is converted to a datastore.Entity
    # 2. datastore.Entity is converted to a protocol buffer object: EntityProto
    # 3. EntityProto is serialized
    #
    # These tests test the various portions of that workflow, as well as the full workflow itself to identify
    # where the performance bottlenecks lie with model serialization/deserialization.
    #
    tests = [
        _benchmark_SINGLE_PROPERTY_ACCESS_TIMES_PROTOBUF_TO_MODEL,
        _benchmark_MULTI_PROPERTY_ACCESS_TIMES_PROTOBUF_TO_MODEL,
        _benchmark_SINGLE_LAZY_PROPERTY_ACCESS_TIMES_PROTOBUF_TO_MODEL,
        _benchmark_MULTI_LAZY_PROPERTY_ACCESS_TIMES_PROTOBUF_TO_MODEL,
        _benchmark_MODEL_TO_PROTOBUF_STRING,
        _benchmark_ENTITY_TO_PROTOBUF_STRING,
        _benchmark_ENTITY_PROTO_TO_PROTOBUF_STRING,
        _benchmark_PROTOBUF_STRING_TO_MODEL,
        _benchmark_PROTOBUF_STRING_TO_ENTITY,
        _benchmark_PROTOBUF_STRING_TO_ENTITY_PROTO,
        # _benchmark_PROTOBUF_STRING_TO_ENTITY_PROTO_WITH_REUSE,

        # _benchmark_PROTOBUF_PROPERTY_SIZE,
    ]
    results = []

    for test in tests:
        for klass in klasses:
            # Execute the test on this model, skipping any tests that are not supported
            try:
                test_group, delta, iterations = test(klass)
                results.append(create_result(klass, test_group, delta, iterations))
            except NotImplementedError:
                pass
    return results


def _benchmark_MODEL_TO_PROTOBUF_STRING(model_class):
    with create_row(model_class) as (row, key):
        def fn():
            entity_proto = row.convert_to_proto()
            entity_proto.SerializeToString()

        seconds = benchmark_fn(fn, SERIALIZATION_ITERATIONS)
        return SerializationTestGroups.MODEL_TO_PROTOBUF_STRING, seconds, SERIALIZATION_ITERATIONS


def _benchmark_ENTITY_TO_PROTOBUF_STRING(model_class):
    with create_row(model_class) as (row, key):
        entity = row.convert_to_entity()

        def fn():
            entity_proto = entity.ToPb()
            entity_proto.SerializeToString()

        seconds = benchmark_fn(fn, SERIALIZATION_ITERATIONS)
        return SerializationTestGroups.ENTITY_TO_PROTOBUF_STRING, seconds, SERIALIZATION_ITERATIONS


def _benchmark_ENTITY_PROTO_TO_PROTOBUF_STRING(model_class):
    with create_row(model_class) as (row, key):
        entity_proto = row.convert_to_proto()

        def fn():
            entity_proto.SerializeToString()

        seconds = benchmark_fn(fn, SERIALIZATION_ITERATIONS)
        return SerializationTestGroups.ENTITY_PROTO_TO_PROTOBUF_STRING, seconds, SERIALIZATION_ITERATIONS


def _benchmark_PROTOBUF_STRING_TO_MODEL(model_class):
    with create_row(model_class) as (row, key):
        entity_proto = row.convert_to_proto()
        serialized = entity_proto.SerializeToString()

        def fn():
            entity_proto = entity_pb.EntityProto(serialized)
            entity = datastore.Entity.FromPb(entity_proto)
            model_class.convert_from_entity(entity)

        seconds = benchmark_fn(fn, SERIALIZATION_ITERATIONS)
        return SerializationTestGroups.PROTOBUF_STRING_TO_MODEL, seconds, SERIALIZATION_ITERATIONS


def _benchmark_PROTOBUF_STRING_TO_ENTITY(model_class):
    with create_row(model_class) as (row, key):
        entity_proto = row.convert_to_proto()
        serialized = entity_proto.SerializeToString()

        def fn():
            entity_proto = entity_pb.EntityProto(serialized)
            datastore.Entity.FromPb(entity_proto)

        seconds = benchmark_fn(fn, SERIALIZATION_ITERATIONS)
        return SerializationTestGroups.PROTOBUF_STRING_TO_ENTITY, seconds, SERIALIZATION_ITERATIONS


def _benchmark_PROTOBUF_STRING_TO_ENTITY_PROTO(model_class):
    with create_row(model_class) as (row, key):
        entity_proto = row.convert_to_proto()
        serialized = entity_proto.SerializeToString()

        def fn():
            entity_proto = entity_pb.EntityProto(serialized)
            datastore.Entity.FromPb(entity_proto)

        seconds = benchmark_fn(fn, SERIALIZATION_ITERATIONS)
        return SerializationTestGroups.PROTOBUF_STRING_TO_ENTITY_PROTO, seconds, SERIALIZATION_ITERATIONS


# def _benchmark_PROTOBUF_STRING_TO_ENTITY_PROTO_WITH_REUSE(model_class):
#     with create_row(model_class) as (row, key):
#         entity_proto = row.convert_to_proto()
#         serialized = entity_proto.SerializeToString()
#
#         def fn():
#             entity_proto.Clear()
#             entity_proto.MergeFromString(serialized)
#
#         seconds = benchmark_fn(fn, SERIALIZATION_ITERATIONS)
#         return SerializationTestGroups.PROTOBUF_STRING_TO_ENTITY_PROTO_WITH_REUSE, seconds, SERIALIZATION_ITERATIONS


def _benchmark_SINGLE_PROPERTY_ACCESS_TIMES_PROTOBUF_TO_MODEL(model_class):
    with create_row(model_class) as (row, key):
        entity_proto = row.convert_to_proto()
        serialized = entity_proto.SerializeToString()

        def fn():
            # entity_proto = entity_pb.EntityProto(serialized)
            # entity = datastore.Entity.FromPb(entity_proto)
            # deserialized = model_class.convert_from_entity(entity)
            entity_proto = entity_pb.EntityProto(serialized)
            deserialized = model_class.convert_from_proto(entity_proto)
            len(deserialized.prop_0)

        seconds = benchmark_fn(fn, SERIALIZATION_ITERATIONS)
        return SerializationTestGroups.SINGLE_PROPERTY_ACCESS_TIMES_PROTOBUF_TO_MODEL, seconds, SERIALIZATION_ITERATIONS


def _benchmark_MULTI_PROPERTY_ACCESS_TIMES_PROTOBUF_TO_MODEL(model_class):
    with create_row(model_class) as (row, key):
        entity_proto = row.convert_to_proto()
        serialized = entity_proto.SerializeToString()

        def fn():
            entity_proto = entity_pb.EntityProto(serialized)
            entity = datastore.Entity.FromPb(entity_proto)
            deserialized = model_class.convert_from_entity(entity)
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
        entity_proto = row.convert_to_proto()
        serialized = entity_proto.SerializeToString()

        def fn():
            entity_proto = entity_pb.EntityProto(serialized)
            deserialized = datastore_lazy.LazyEntity(entity_proto)
            len(deserialized.prop_0)

        seconds = benchmark_fn(fn, SERIALIZATION_ITERATIONS)
        return SerializationTestGroups.SINGLE_LAZY_PROPERTY_ACCESS_TIMES_PROTOBUF_TO_MODEL, seconds, SERIALIZATION_ITERATIONS


def _benchmark_MULTI_LAZY_PROPERTY_ACCESS_TIMES_PROTOBUF_TO_MODEL(model_class):
    with create_row(model_class) as (row, key):
        entity_proto = row.convert_to_proto()
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

# def _benchmark_PROTOBUF_PROPERTY_SIZE(model_class):
#     with create_row(model_class) as (row, key):
#         entity_proto = row.convert_to_proto()
#         serialized = entity_proto.SerializeToString()
#
#         def fn():
#             entity_proto = entity_pb.EntityProto(serialized)
#             entity_proto.property_size()
#
#         seconds = benchmark_fn(fn, SERIALIZATION_ITERATIONS)
#         return SerializationTestGroups.PROTOBUF_PROPERTY_SIZE, seconds, SERIALIZATION_ITERATIONS
