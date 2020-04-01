from __future__ import absolute_import
import unittest

import os.path
import unittest

from datastore_performance.benchmark_serialization import _benchmark_MODEL_TO_PROTOBUF_STRING
from datastore_performance.models import Model10
from google.appengine.datastore import datastore_stub_index
from google.appengine.ext import testbed

from datastore_performance import benchmark_crud, constants
from datastore_performance.constants import DB_MODEL_CLASSES

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
    _testbed.init_taskqueue_stub(enable=True, root_path='.')
    _index_yaml_path = os.path.join(".")
    _index_updater = datastore_stub_index.IndexYamlUpdater(_index_yaml_path)


def tearDownModule():
    global _testbed, _index_updater
    # We need to create a new updater instance for every test because
    # the datastore is cleared on test setup.
    _index_updater.UpdateIndexYaml()
    _testbed.deactivate()


class TestFormatCsv(unittest.TestCase):
    def test_format_csv_1x(self):
        result = _benchmark_MODEL_TO_PROTOBUF_STRING(Model10)
        csv_string = constants.format_csv([result])
        self.assertEqual(len(csv_string.split("\n")), 2)
