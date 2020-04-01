from __future__ import absolute_import

from google.appengine.datastore import entity_pb
from google.appengine.ext import ndb


class NdbQueryMixin(object):

    @classmethod
    def keys(cls, limit):
        return cls.query().fetch(limit, keys_only=True)

    @classmethod
    def get(cls, keys):
        # Disable NDB's caching since it bypasses all deserialization, which is what we want to measure
        return ndb.get_multi(keys, use_cache=False, use_memcache=False)

    @classmethod
    def put(cls, models):
        return ndb.put_multi(models)

    @classmethod
    def delete(cls, models):
        keys = map(lambda x: x.key, models)
        return ndb.delete_multi(keys)

    def convert_to_entity(self):
        raise NotImplementedError("Conversion to db.Entity is not supported")

    def convert_to_proto(self):
        return self._to_pb()

    @classmethod
    def convert_from_binary(cls, serialized):
        entity_proto = entity_pb.EntityProto(serialized)
        return cls.convert_from_proto(entity_proto)

    @classmethod
    def convert_from_proto(cls, proto):
        return cls._from_pb(proto)

    @classmethod
    def convert_from_entity(cls, entity):
        raise NotImplementedError("Conversion from db.Entity is not supported")
