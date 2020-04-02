from __future__ import absolute_import

from google.appengine.api import datastore
from google.appengine.datastore import entity_pb
from google.appengine.ext import db

from datastore_performance import datastore_lazy


class DbQueryMixin(object):
    @classmethod
    def keys(cls, limit):
        return list(cls.all(keys_only=True).run(limit=limit, batch_size=limit))

    @classmethod
    def get_async(cls, keys):
        keys, multiple = datastore.NormalizeAndTypeCheckKeys(keys)

        rpc = datastore.GetAsync(keys)
        results = rpc.get_result()
        return results if multiple else results[0]

    @classmethod
    def get_lazy(cls, keys):
        keys, multiple = datastore.NormalizeAndTypeCheckKeys(keys)
        results = datastore_lazy.get(keys)
        return results if multiple else results[0]

    @classmethod
    def put(cls, models):
        db.put(models)

    @classmethod
    def delete(cls, models):
        db.delete(models)

    def convert_to_proto(self):
        return self.convert_to_entity().ToPb()

    def convert_to_entity(self):
        return self._populate_entity()

    @classmethod
    def convert_from_binary(cls, binary):
        entity_proto = entity_pb.EntityProto(binary)
        return cls.convert_from_proto(entity_proto)

    @classmethod
    def convert_from_proto(cls, entity_proto):
        entity = datastore.Entity.FromPb(entity_proto)
        return cls.convert_from_entity(entity)

    @classmethod
    def convert_from_entity(cls, entity):
        return cls.from_entity(entity)
