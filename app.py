from __future__ import absolute_import

import csv
from StringIO import StringIO

from flask import Flask, render_template, make_response
from marshmallow import Schema, fields

from datastore_performance.benchmark_crud import benchmark_crud_models
from datastore_performance.benchmark_serialization import benchmark_serialization_models
from datastore_performance.constants import format_csv


class TestRunResult(Schema):
    klass = fields.String(required=True)
    properties_count = fields.Integer(required=True)
    test_group = fields.String(required=True)
    row_count = fields.Integer(required=True)
    iteration_count = fields.Integer(required=True)
    total_milli_seconds = fields.Float(required=True)
    avg_milli_seconds = fields.Float(required=True)


app = Flask(__name__)


@app.route('/')
def hello():
    return "Hello World!"


@app.route('/benchmark/serialization', defaults={'format': 'html'})
@app.route('/benchmark/serialization.<format>')
def benchmark_serialization(format):
    results = benchmark_serialization_models()
    if format == 'csv':
        return _render_csv(results, 'benchmark_serialization.remote.csv')
    elif format == 'html':
        return _render_html(results)
    else:
        return TestRunResult().dump(results, many=True)


@app.route('/benchmark/crud', defaults={'format': 'html', 'run_test_groups': None})
@app.route('/benchmark/crud.<format>', defaults={'run_test_groups': None})
@app.route('/benchmark/crud/<run_test_groups>', defaults={'format': 'html'})
@app.route('/benchmark/crud/<run_test_groups>.<format>')
def benchmark_crud(run_test_groups, format):
    if run_test_groups:
        run_test_groups = tuple(filter(lambda x: x, run_test_groups.upper().split(',')))

    results = benchmark_crud_models(run_test_groups=run_test_groups)
    if format == 'csv':
        return _render_csv(results, 'benchmark_crud.remote.csv')
    elif format == 'html':
        return _render_html(results)
    else:
        return TestRunResult().dump(results, many=True)


def _render_csv(results, file_name):
    output = format_csv(results)
    response = make_response(output)
    response.headers["Content-Disposition"] = "attachment; filename={}".format(file_name)
    response.headers["Content-type"] = "text/csv"
    return response


def _render_html(results):
    output = format_csv(results)
    string_buffer = StringIO(output)
    reader = csv.reader(string_buffer, delimiter=',')
    rows = [row for row in reader]
    return render_template('results.jinja2', header=rows[0], rows=rows[1:])


if __name__ == '__main__':
    app.run()
