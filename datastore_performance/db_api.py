from __future__ import absolute_import

from google.appengine.ext import db


class DbQueryMixin(object):
    @classmethod
    def keys(cls, limit):
        return list(cls.all(keys_only=True).run(limit=limit, batch_size=limit))

    @classmethod
    def put(cls, models):
        db.put(models)

    @classmethod
    def delete(cls, models):
        db.delete(models)
