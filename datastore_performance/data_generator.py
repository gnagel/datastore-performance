from __future__ import absolute_import

import time
import uuid
from contextlib import contextmanager


@contextmanager
def create_row(model_class):
    row = model_class()
    for property in row._properties.keys():
        setattr(row, property, str(uuid.uuid4()))
    row.put()

    # Wait till the data syncs to Datastore
    while not model_class.get(row.key()):
        time.sleep(0.5)

    try:
        yield row
    finally:
        row.delete()


@contextmanager
def create_rows(model_class, count):
    rows = []
    for _ in range(count):
        row = model_class()
        for property in row._properties.keys():
            setattr(row, property, str(uuid.uuid4()))
        row.put()

    # Wait till the data syncs to Datastore
    while len(model_class.get(map(lambda row: row.key(), rows))) != len(rows):
        time.sleep(0.5)

    try:
        yield rows
    finally:
        for row in rows:
            row.delete()
