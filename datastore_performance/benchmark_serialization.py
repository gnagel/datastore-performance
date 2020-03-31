from __future__ import absolute_import

import time
import uuid

import enum
from google.appengine.api import datastore
from google.appengine.datastore import entity_pb

from datastore_performance import datastore_lazy
from datastore_performance.constants import INSTANCES_TO_CREATE, MODEL_CLASSES, DB_MODEL_CLASSES, \
    SERIALIZATION_ITERATIONS, create_result
from datastore_performance.data_generator import create_row


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


def seed_database_rows():
    for model_class in MODEL_CLASSES:
        for _ in range(INSTANCES_TO_CREATE):
            row = model_class()
            for property in row._properties.keys():
                setattr(row, property, str(uuid.uuid4()))
            row.put()
    return INSTANCES_TO_CREATE * len(MODEL_CLASSES)


def benchmark_serialization_models():
    results = []
    for klass in DB_MODEL_CLASSES:
        results.extend(_benchmark_serialization(klass))
    return results


def _benchmark_MODEL_TO_PROTOBUF_STRING(model_class):
    with create_row(model_class) as row:
        start = time.time()
        for _ in range(SERIALIZATION_ITERATIONS):
            entity = row._populate_entity(datastore.Entity)
            entity_proto = entity.ToPb()
            entity_proto.SerializeToString()
        end = time.time()

    return SerializationTestGroups.MODEL_TO_PROTOBUF_STRING, float(end - start)


def _benchmark_ENTITY_TO_PROTOBUF_STRING(model_class):
    with create_row(model_class) as row:
        entity = row._populate_entity(datastore.Entity)
        start = time.time()
        for _ in range(SERIALIZATION_ITERATIONS):
            entity_proto = entity.ToPb()
            entity_proto.SerializeToString()
        end = time.time()

    return SerializationTestGroups.ENTITY_TO_PROTOBUF_STRING, float(end - start)


def _benchmark_ENTITY_PROTO_TO_PROTOBUF_STRING(model_class):
    with create_row(model_class) as row:
        entity = row._populate_entity(datastore.Entity)
        entity_proto = entity.ToPb()
        start = time.time()
        for _ in range(SERIALIZATION_ITERATIONS):
            entity_proto.SerializeToString()
        end = time.time()
    return SerializationTestGroups.ENTITY_PROTO_TO_PROTOBUF_STRING, float(end - start)


def _benchmark_PROTOBUF_STRING_TO_MODEL(model_class):
    with create_row(model_class) as row:
        entity = row._populate_entity(datastore.Entity)
        entity_proto = entity.ToPb()
        serialized = entity_proto.SerializeToString()
        start = time.time()
        for _ in range(SERIALIZATION_ITERATIONS):
            entity_proto = entity_pb.EntityProto(serialized)
            entity = datastore.Entity.FromPb(entity_proto)
            model_class.from_entity(entity)
        end = time.time()
    return SerializationTestGroups.PROTOBUF_STRING_TO_MODEL, float(end - start)


def _benchmark_PROTOBUF_STRING_TO_ENTITY(model_class):
    with create_row(model_class) as row:
        entity = row._populate_entity(datastore.Entity)
        entity_proto = entity.ToPb()
        serialized = entity_proto.SerializeToString()
        start = time.time()
        for _ in range(SERIALIZATION_ITERATIONS):
            entity_proto = entity_pb.EntityProto(serialized)
            datastore.Entity.FromPb(entity_proto)
        end = time.time()
    return SerializationTestGroups.PROTOBUF_STRING_TO_ENTITY, float(end - start)


def _benchmark_PROTOBUF_STRING_TO_ENTITY_PROTO(model_class):
    with create_row(model_class) as row:
        entity = row._populate_entity(datastore.Entity)
        entity_proto = entity.ToPb()
        serialized = entity_proto.SerializeToString()
        start = time.time()
        for _ in range(SERIALIZATION_ITERATIONS):
            entity_proto = entity_pb.EntityProto(serialized)
            datastore.Entity.FromPb(entity_proto)
        end = time.time()
    return SerializationTestGroups.PROTOBUF_STRING_TO_ENTITY_PROTO, float(end - start)


def _benchmark_PROTOBUF_STRING_TO_ENTITY_PROTO_WITH_REUSE(model_class):
    with create_row(model_class) as row:
        entity = row._populate_entity(datastore.Entity)
        entity_proto = entity.ToPb()
        serialized = entity_proto.SerializeToString()
        start = time.time()
        for _ in range(SERIALIZATION_ITERATIONS):
            entity_proto.Clear()
            entity_proto.MergeFromString(serialized)
        end = time.time()
    return SerializationTestGroups.PROTOBUF_STRING_TO_ENTITY_PROTO_WITH_REUSE, float(end - start)


def _benchmark_SINGLE_PROPERTY_ACCESS_TIMES_PROTOBUF_TO_MODEL(model_class):
    with create_row(model_class) as row:
        entity = row._populate_entity(datastore.Entity)
        entity_proto = entity.ToPb()
        serialized = entity_proto.SerializeToString()
        start = time.time()
        for _ in range(SERIALIZATION_ITERATIONS):
            entity_proto = entity_pb.EntityProto(serialized)
            entity = datastore.Entity.FromPb(entity_proto)
            deserialized = model_class.from_entity(entity)
            len(deserialized.prop_0)
        end = time.time()
    return SerializationTestGroups.SINGLE_PROPERTY_ACCESS_TIMES_PROTOBUF_TO_MODEL, float(end - start)


def _benchmark_MULTI_PROPERTY_ACCESS_TIMES_PROTOBUF_TO_MODEL(model_class):
    with create_row(model_class) as row:
        entity = row._populate_entity(datastore.Entity)
        entity_proto = entity.ToPb()
        serialized = entity_proto.SerializeToString()
        start = time.time()
        for _ in range(SERIALIZATION_ITERATIONS):
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
        end = time.time()

    return SerializationTestGroups.MULTI_PROPERTY_ACCESS_TIMES_PROTOBUF_TO_MODEL, float(end - start)


def _benchmark_SINGLE_LAZY_PROPERTY_ACCESS_TIMES_PROTOBUF_TO_MODEL(model_class):
    with create_row(model_class) as row:
        entity = row._populate_entity(datastore.Entity)
        entity_proto = entity.ToPb()
        serialized = entity_proto.SerializeToString()
        start = time.time()
        for _ in range(SERIALIZATION_ITERATIONS):
            entity_proto = entity_pb.EntityProto(serialized)
            deserialized = datastore_lazy.LazyEntity(entity_proto)
            len(deserialized.prop_0)
        end = time.time()
    return SerializationTestGroups.SINGLE_LAZY_PROPERTY_ACCESS_TIMES_PROTOBUF_TO_MODEL, float(end - start)


def _benchmark_MULTI_LAZY_PROPERTY_ACCESS_TIMES_PROTOBUF_TO_MODEL(model_class):
    with create_row(model_class) as row:
        entity = row._populate_entity(datastore.Entity)
        entity_proto = entity.ToPb()
        serialized = entity_proto.SerializeToString()
        start = time.time()
        for _ in range(SERIALIZATION_ITERATIONS):
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
        end = time.time()
    return SerializationTestGroups.MULTI_LAZY_PROPERTY_ACCESS_TIMES_PROTOBUF_TO_MODEL, float(end - start)


def _benchmark_PROTOBUF_PROPERTY_SIZE(model_class):
    with create_row(model_class) as row:
        entity = row._populate_entity(datastore.Entity)
        entity_proto = entity.ToPb()
        serialized = entity_proto.SerializeToString()
        start = time.time()
        for _ in range(SERIALIZATION_ITERATIONS):
            entity_proto = entity_pb.EntityProto(serialized)
            entity_proto.property_size()
        end = time.time()
    return SerializationTestGroups.PROTOBUF_PROPERTY_SIZE, float(end - start)


def _benchmark_serialization(model_class):
    # How data gets from a db.Model subclass to bytes:
    # 1. db.Model is converted to a datastore.Entity
    # 2. datastore.Entity is converted to a protocol buffer object: EntityProto
    # 3. EntityProto is serialized

    results = []

    test_group, delta = _benchmark_MODEL_TO_PROTOBUF_STRING(model_class)
    results.append(create_result(model_class, test_group, delta))

    test_group, delta = _benchmark_ENTITY_TO_PROTOBUF_STRING(model_class)
    results.append(create_result(model_class, test_group, delta))

    test_group, delta = _benchmark_ENTITY_PROTO_TO_PROTOBUF_STRING(model_class)
    results.append(create_result(model_class, test_group, delta))

    test_group, delta = _benchmark_PROTOBUF_STRING_TO_MODEL(model_class)
    results.append(create_result(model_class, test_group, delta))

    test_group, delta = _benchmark_PROTOBUF_STRING_TO_ENTITY(model_class)
    results.append(create_result(model_class, test_group, delta))

    test_group, delta = _benchmark_PROTOBUF_STRING_TO_ENTITY_PROTO(model_class)
    results.append(create_result(model_class, test_group, delta))

    test_group, delta = _benchmark_PROTOBUF_STRING_TO_ENTITY_PROTO_WITH_REUSE(model_class)
    results.append(create_result(model_class, test_group, delta))

    test_group, delta = _benchmark_SINGLE_PROPERTY_ACCESS_TIMES_PROTOBUF_TO_MODEL(model_class)
    results.append(create_result(model_class, test_group, delta))

    test_group, delta = _benchmark_MULTI_PROPERTY_ACCESS_TIMES_PROTOBUF_TO_MODEL(model_class)
    results.append(create_result(model_class, test_group, delta))

    test_group, delta = _benchmark_SINGLE_LAZY_PROPERTY_ACCESS_TIMES_PROTOBUF_TO_MODEL(model_class)
    results.append(create_result(model_class, test_group, delta))

    test_group, delta = _benchmark_MULTI_LAZY_PROPERTY_ACCESS_TIMES_PROTOBUF_TO_MODEL(model_class)
    results.append(create_result(model_class, test_group, delta))

    test_group, delta = _benchmark_PROTOBUF_PROPERTY_SIZE(model_class)
    results.append(create_result(model_class, test_group, delta))

    return results
