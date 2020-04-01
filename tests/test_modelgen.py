from __future__ import absolute_import

import unittest

from google.appengine.ext import db
from google.appengine.ext import ndb

from datastore_performance import models


class SomeModel(db.Model):
    foo = db.StringProperty(indexed=False)
    bar = db.StringProperty(indexed=False)


class Test(unittest.TestCase):
    def test_generated_models(self):
        model_types = [
            (models.PgModel10, 10, db.Model,),
            (models.PgModel100, 100, db.Model,),
            (models.Model10, 10, db.Model,),
            (models.Model100, 100, db.Model,),
            (models.Expando10, 10, db.Expando,),
            (models.Expando100, 100, db.Expando,),
            (models.NdbModel10, 10, ndb.Model,),
            (models.NdbModel100, 100, ndb.Model,),
            (models.NdbExpando10, 10, ndb.Expando,),
            (models.NdbExpando100, 100, ndb.Expando,),
        ]
        for (klass, properties_count, base_class) in model_types:
            self.assertIsInstance(klass(), base_class)
            self.assertEqual(properties_count, len(klass._properties.keys()))
