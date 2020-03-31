from __future__ import absolute_import

from collections import namedtuple

from datastore_performance import models

TestRunResult = namedtuple('TestRunResult', [
    'klass',
    'properties_count',
    'test_group',
    'row_count',
    'iteration_count',
    'total_milli_seconds',
    'avg_milli_seconds',
])


def create_result(model_class, test_group, delta):
    return TestRunResult(
        klass=model_class.__name__,
        properties_count=len(model_class._properties.keys()),
        test_group=test_group.value,
        row_count=1,
        iteration_count=SERIALIZATION_ITERATIONS,
        total_milli_seconds=delta,
        avg_milli_seconds=delta / float(SERIALIZATION_ITERATIONS),
    )


DB_MODEL_CLASSES = [
    models.Model10,
    models.Model100,
    models.Expando10,
    models.Expando100,
]
NDB_MODEL_CLASSES = [
    models.NdbModel10,
    models.NdbModel100,
    models.NdbExpando10,
    models.NdbExpando100,
]
MODEL_CLASSES = DB_MODEL_CLASSES + NDB_MODEL_CLASSES

INSTANCES_TO_CREATE = 100
NUM_INSTANCES_TO_DESERIALIZE = 20
SERIALIZATION_ITERATIONS = 100
READ_ITERATIONS = 100