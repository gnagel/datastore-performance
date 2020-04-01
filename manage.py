from __future__ import absolute_import

import click
from jinja2 import Template

from datastore_performance.benchmark_crud import benchmark_crud_models
from datastore_performance.benchmark_serialization import benchmark_serialization_models
from datastore_performance.constants import format_csv
from test_benchmark_crud import setUpModule, tearDownModule


@click.group()
def generate():
    pass


@generate.command()
def generate_models():
    with open('/app/datastore_performance/templates/models.jinja2', 'r') as file_handle:
        template_src = file_handle.read()

    template = Template(template_src)
    code = template.render()
    with open('/app/datastore_performance/models.py', 'w') as file_handle:
        file_handle.write(code)


@generate.command()
def benchmark_serialization():
    setUpModule()
    results = benchmark_serialization_models()
    tearDownModule()

    csv_string = format_csv(results)

    with open('benchmark_serialization.csv', 'w') as file_handle:
        file_handle.write(csv_string)


@generate.command()
def benchmark_crud():
    setUpModule()
    results = benchmark_crud_models()
    tearDownModule()

    csv_string = format_csv(results)

    with open('benchmark_crud.csv', 'w') as file_handle:
        file_handle.write(csv_string)


if __name__ == "__main__":
    generate()
