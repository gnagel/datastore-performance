from __future__ import absolute_import

import os.path
import unittest

from google.appengine.datastore import datastore_stub_index
from google.appengine.ext import testbed

from datastore_performance import benchmark_serialization
from datastore_performance.constants import model_classes
from datastore_performance.models import PgModel10, PgModel100

_testbed = None
_index_yaml_path = None
_index_updater = None



def setUpModule():
    global _testbed, _index_yaml_path, _index_updater
    _testbed = testbed.Testbed()
    _testbed.activate()
    _testbed.init_datastore_v3_stub()
    _testbed.init_memcache_stub()
    _testbed.init_search_stub()
    _testbed.init_app_identity_stub()
    _testbed.init_urlfetch_stub()
    _testbed.init_blobstore_stub()
    _testbed.init_taskqueue_stub(enable=True, root_path='..')
    _index_yaml_path = os.path.join("..")
    _index_updater = datastore_stub_index.IndexYamlUpdater(_index_yaml_path)

    PgModel10.delete_table()
    PgModel100.delete_table()

    PgModel10.initalize_table()
    PgModel100.initalize_table()


def tearDownModule():
    global _testbed, _index_updater
    # We need to create a new updater instance for every test because
    # the datastore is cleared on test setup.
    _index_updater.UpdateIndexYaml()
    _testbed.deactivate()

    PgModel10.delete_table()
    PgModel100.delete_table()


class TestBenchmarkSerializationModels(unittest.TestCase):
    def test_benchmark_serialization_models(self):
        klasses = model_classes()[:2]
        output = benchmark_serialization.benchmark_serialization_models(klasses)
        count_models = len(klasses)
        count_test_groups = len([x for x in benchmark_serialization.SerializationTestGroups])
        self.assertEqual(len(output), count_models * count_test_groups)
