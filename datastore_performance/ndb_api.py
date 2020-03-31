from __future__ import absolute_import

from google.appengine.ext import ndb


class NdbQueryMixin(object):

    @classmethod
    def keys(cls, limit):
        return cls.query().fetch(limit, keys_only=True)


    @classmethod
    def get(cls, keys):
        # Disable NDB's caching since it bypasses all deserialization, which is what we want to measure
        return ndb.get_multi(keys, use_cache=False, use_memcache=False)
