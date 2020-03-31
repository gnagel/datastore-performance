from __future__ import absolute_import


def get(klass, key_strings):
    pass


def put(klass, models):
    pass


def delete(klass, models):
    pass

class PgQueryMixin(object):

    @classmethod
    def get(cls, keys):
        keys, multiple = NormalizeAndTypeCheckKeys(keys)
        results = get(cls, keys)
        if multiple:
            return results
        else:
            return results[0]

    @classmethod
    def put(cls, models):
        results = put(cls, models)
        multiple = isinstance(models, list)
        if multiple:
            return results
        else:
            return results[0]

    @classmethod
    def delete(cls, models):
        delete(cls, models)

    def put(self):
        self.__class__.put([self])

    def delete(self):
        self.__class__.delete([self])
