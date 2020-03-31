from __future__ import absolute_import

from flask import Flask
from marshmallow import Schema, fields

from datastore_performance import DbEntitySetup, DbEntityTest, SerializationTest


class TestRunResult(Schema):
    test_group = fields.String(required=True)
    row_count = fields.Integer(required=True)
    milli_seconds = fields.Float(required=True)


class TestSummary(Schema):
    test_runs = fields.Nested(TestRunResult, many=True)
    test_summary = fields.Nested(TestRunResult, many=True)


app = Flask(__name__)


@app.route('/')
def hello():
    return "Hello World!"


@app.route('/db_entity_setup')
def db_entity_setup():
    DbEntitySetup(500)
    return "Entities Created"


@app.route('/db_entity_test')
def db_entity_test():
    DbEntityTest()
    return "Executed test runs"


@app.route('/serialization_test')
def serialization_test()
    SerializationTest()
    return "Executed serializtion tests"


if __name__ == '__main__':
    app.run()
