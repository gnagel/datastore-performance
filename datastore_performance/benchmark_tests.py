from __future__ import absolute_import

import time
import uuid

import enum
from google.appengine.api import datastore
from google.appengine.datastore import entity_pb

from datastore_performance.constants import INSTANCES_TO_CREATE, MODEL_CLASSES, DB_MODEL_CLASSES, \
    SERIALIZATION_ITERATIONS, create_result


@enum.uniqe
class SerializationTestGroups(enum.Enum):
    MODEL_to_PROTOBUF_STRING = 'serialize: model -> db.Entity -> entity_pb.EntityProto -> Protobuf string'
    ENTITY_to_PROTOBUF_STRING = 'serialize: db.Entity -> entity_pb.EntityProto -> Protobuf string'
    ENTITY_PROTO_to_PROTOBUF_STRING = 'serialize: entity_pb.EntityProto -> Protobuf string'

    PROTOBUF_STRING_to_MODEL = 'deserialize: Protobuf string --> model --> entity_pb.EntityProto --< db.Entity'
    PROTOBUF_STRING_to_ENTITY = 'deserialize: Protobuf string --> db.Entity <- entity_pb.EntityProto'
    PROTOBUF_STRING_to_ENTITY_PROTO = 'deserialize: Protobuf string --> entity_pb.EntityProto'
    PROTOBUF_STRING_to_ENTITY_PROTO_WITH_REUSE = 'deserialize: Protobuf string --> entity_pb.EntityProto with protobuf reuse'

    PROPERTY_ACCESS_TIMES_PROTOBUF_TO_MODEL = '1x property access time, deserialize: entity_pb.EntityProto <- Protobuf string with protobuf reuse'


def seed_database_rows():
    for model_class in MODEL_CLASSES:
        rows = []
        for _ in range(INSTANCES_TO_CREATE):
            row = model_class()
            for property in row._properties.keys():
                setattr(row, property, str(uuid.uuid4()))
            rows.append(row)
        model_class.put(rows)
    return INSTANCES_TO_CREATE * len(MODEL_CLASSES)


def benchmark_serialization_models():
    results = []
    for klass in DB_MODEL_CLASSES:
        keys = klass.keys(1)
        row = klass.get(keys[0])
        results.extend(_benchmark_serialization(row))
    return results


def _benchmark_MODEL_TO_PROTOBUF_STRING(model_instance):
    start = time.time()
    for _ in range(SERIALIZATION_ITERATIONS):
        entity = model_instance._populate_entity(datastore.Entity)
        entity_proto = entity.ToPb()
        entity_proto.SerializeToString()
    end = time.time()

    return SerializationTestGroups.MODEL_TO_PROTOBUF_STRING, float(end - start)


def _benchmark_ENTITY_TO_PROTOBUF_STRING(model_instance):
    entity = model_instance._populate_entity(datastore.Entity)

    start = time.time()
    for _ in range(SERIALIZATION_ITERATIONS):
        entity_proto = entity.ToPb()
        entity_proto.SerializeToString()
    end = time.time()

    return SerializationTestGroups.ENTITY_TO_PROTOBUF_STRING, float(end - start)


def _benchmark_ENTITY_PROTO_TO_PROTOBUF_STRING(model_instance):
    entity = model_instance._populate_entity(datastore.Entity)
    entity_proto = entity.ToPb()

    start = time.time()
    for _ in range(SERIALIZATION_ITERATIONS):
        entity_proto.SerializeToString()
    end = time.time()

    return SerializationTestGroups.ENTITY_PROTO_TO_PROTOBUF_STRING, float(end - start)


def _benchmark_PROTOBUF_STRING_to_MODEL(model_instance):
    entity = model_instance._populate_entity(datastore.Entity)
    entity_proto = entity.ToPb()
    serialized = entity_proto.SerializeToString()

    start = time.time()
    for _ in range(SERIALIZATION_ITERATIONS):
        entity_proto = entity_pb.EntityProto(serialized)
        entity = datastore.Entity.FromPb(entity_proto)
        model_instance.__class__.from_entity(entity)
    end = time.time()

    return SerializationTestGroups.PROTOBUF_STRING_to_MODEL, float(end - start)


def _benchmark_PROTOBUF_STRING_to_ENTITY(model_instance):
    entity = model_instance._populate_entity(datastore.Entity)
    entity_proto = entity.ToPb()
    serialized = entity_proto.SerializeToString()

    start = time.time()
    for _ in range(SERIALIZATION_ITERATIONS):
        entity_proto = entity_pb.EntityProto(serialized)
        datastore.Entity.FromPb(entity_proto)
    end = time.time()

    return SerializationTestGroups.PROTOBUF_STRING_to_ENTITY, float(end - start)


def _benchmark_PROTOBUF_STRING_to_ENTITY_PROTO(model_instance):
    entity = model_instance._populate_entity(datastore.Entity)
    entity_proto = entity.ToPb()
    serialized = entity_proto.SerializeToString()

    start = time.time()
    for _ in range(SERIALIZATION_ITERATIONS):
        entity_proto = entity_pb.EntityProto(serialized)
        datastore.Entity.FromPb(entity_proto)
    end = time.time()

    return SerializationTestGroups.PROTOBUF_STRING_to_ENTITY_PROTO, float(end - start)


def _benchmark_PROTOBUF_STRING_to_ENTITY_PROTO_WITH_REUSE(model_instance):
    entity = model_instance._populate_entity(datastore.Entity)
    entity_proto = entity.ToPb()
    serialized = entity_proto.SerializeToString()

    start = time.time()
    for _ in range(SERIALIZATION_ITERATIONS):
        entity_proto.Clear()
        entity_proto.MergeFromString(serialized)
    end = time.time()

    return SerializationTestGroups.PROTOBUF_STRING_to_ENTITY_PROTO_WITH_REUSE, float(end - start)


def _benchmark_serialization(model_instance):
    # How data gets from a db.Model subclass to bytes:
    # 1. db.Model is converted to a datastore.Entity
    # 2. datastore.Entity is converted to a protocol buffer object: EntityProto
    # 3. EntityProto is serialized

    results = []

    test_group, delta = _benchmark_MODEL_TO_PROTOBUF_STRING(model_instance)
    results.append(create_result(model_instance, test_group, delta))

    test_group, delta = _benchmark_ENTITY_TO_PROTOBUF_STRING(model_instance)
    results.append(create_result(model_instance, test_group, delta))

    test_group, delta = _benchmark_ENTITY_PROTO_TO_PROTOBUF_STRING(model_instance)
    results.append(create_result(model_instance, test_group, delta))

    test_group, delta = _benchmark_PROTOBUF_STRING_to_MODEL(model_instance)
    results.append(create_result(model_instance, test_group, delta))

    test_group, delta = _benchmark_PROTOBUF_STRING_to_ENTITY(model_instance)
    results.append(create_result(model_instance, test_group, delta))

    test_group, delta = _benchmark_PROTOBUF_STRING_to_ENTITY_PROTO(model_instance)
    results.append(create_result(model_instance, test_group, delta))

    test_group, delta = _benchmark_PROTOBUF_STRING_to_ENTITY_PROTO_WITH_REUSE(model_instance)
    results.append(create_result(model_instance, test_group, delta))

    # model / LazyEntity property access tests
    response.write('\n### model / LazyEntity property access times\n')
    total_length = 0
    start = time.time()
    for _ in range(SERIALIZATION_ITERATIONS):
        entity_proto = entity_pb.EntityProto(serialized)
        entity = datastore.Entity.FromPb(entity_proto)
        # from model_from_protobuf
        deserialized = db.class_for_kind(entity.kind()).from_entity(entity)
        total_length += len(deserialized.prop_a)
    end = time.time()
    output(response,
           'model deserialized and accessed one property %d times in %f s' % (SERIALIZATION_ITERATIONS, end - start))

    total_length = 0
    start = time.time()
    for _ in range(SERIALIZATION_ITERATIONS):
        entity_proto = entity_pb.EntityProto(serialized)
        entity = datastore.Entity.FromPb(entity_proto)
        # from model_from_protobuf
        deserialized = db.class_for_kind(entity.kind()).from_entity(entity)
        total_length += len(deserialized.prop_a)
        total_length += len(deserialized.prop_b)
        total_length += len(deserialized.prop_c)
        total_length += len(deserialized.prop_d)
        total_length += len(deserialized.prop_e)
    end = time.time()
    output(response,
           'model deserialized and accessed five properties %d times in %f s' % (SERIALIZATION_ITERATIONS, end - start))

    total_length = 0
    start = time.time()
    for _ in range(SERIALIZATION_ITERATIONS):
        entity_proto = entity_pb.EntityProto(serialized)
        deserialized = datastore_lazy.LazyEntity(entity_proto)
        total_length += len(deserialized.prop_a)
    end = time.time()
    output(response, 'LazyEntity deserialized and accessed one property %d times in %f s' % (
        SERIALIZATION_ITERATIONS, end - start))

    total_length = 0
    start = time.time()
    for _ in range(SERIALIZATION_ITERATIONS):
        entity_proto = entity_pb.EntityProto(serialized)
        deserialized = datastore_lazy.LazyEntity(entity_proto)
        total_length += len(deserialized.prop_a)
        total_length += len(deserialized.prop_b)
        total_length += len(deserialized.prop_c)
        total_length += len(deserialized.prop_d)
        total_length += len(deserialized.prop_e)
    end = time.time()
    output(response, 'LazyEntity deserialized and accessed five properties %d times in %f s' % (
        SERIALIZATION_ITERATIONS, end - start))

    response.write('\n### protocol buffer / pure python access times\n')
    total = 0
    start = time.time()
    for _ in range(SERIALIZATION_ITERATIONS):
        total += entity_proto.property_size()
    end = time.time()
    output(response, 'protocol buffer entity_proto.property_size access in %f s' % (end - start))
