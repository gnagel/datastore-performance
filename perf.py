from __future__ import absolute_import

import logging
import time

import webapp2
from google.appengine.api import datastore
from google.appengine.ext import db
from google.appengine.ext import ndb

import datastore_lazy

# Produces lots of output but lets you view what the entities actually look like
DUMP_ENTITIES = False


def output(response, message):
    response.write(message + '\n')
    logging.info(message)


ITERATIONS = 10


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
    if len(keys) == 0:
        response.write("\n\n### ERROR NO ENTITIES ###")
        return

    bench(response, model_class, keys)



class DbEntityTest(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain;charset=UTF-8'

        for model_class in MODEL_CLASSES:
            self.response.write('\n\n## %s:\n' % (model_class.__name__))
            find_keys_and_bench(self.response, model_class)


class SerializationTest(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain;charset=UTF-8'

        for model_class in DB_MODEL_CLASSES:
            q = db.Query(model_class)
            instance = q.get()
            self.response.write('\n\n## %s:\n' % (model_class.__name__))
            benchmark_serialization(self.response, instance)


app = webapp2.WSGIApplication([
    ('/db_entity_setup', DbEntitySetup),
    ('/db_entity_test', DbEntityTest),
    ('/serialization_test', SerializationTest),
])
