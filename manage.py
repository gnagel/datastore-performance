from __future__ import absolute_import

import logging
import os
import time
import urllib2

import click
from jinja2 import Template

from datastore_performance.benchmark_crud import benchmark_crud_models
from datastore_performance.benchmark_serialization import benchmark_serialization_models
from datastore_performance.constants import format_csv
from tests.test_benchmark_crud import setUpModule, tearDownModule


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
    application_id = os.environ.get('APPLICATION_ID', None)
    # Initialize either the mock stubs, or a remote connection to app engine
    if not application_id:
        click.echo('Using mock app-engine APIs')
        setUpModule()
    else:
        click.echo('Connection to App Engine: {}'.format(application_id))
        _boot_app_engine(application_id)

    results = benchmark_crud_models()

    if not application_id:
        tearDownModule()

    csv_string = format_csv(results)

    with open('benchmark_crud.csv', 'w') as file_handle:
        file_handle.write(csv_string)


def _boot_app_engine(project_id):
    #
    # Boot the App Engine environment
    #

    # This makes the GCS work!
    # http://stackoverflow.com/questions/22646641/google-cloud-storage-client-with-remote-api-on-local-client
    os.environ["SERVER_SOFTWARE"] = ""
    os.environ["HTTP_HOST"] = project_id + '.appspot.com'

    # Always use UTC here so entities timestamps get updated with UTC
    os.environ['TZ'] = 'UTC'
    time.tzset()

    from google.appengine.ext.remote_api import remote_api_stub

    try:
        remote_api_stub.ConfigureRemoteApiForOAuth(os.environ["HTTP_HOST"], '/_ah/remote_api')
    except urllib2.HTTPError as e:
        click.echo("ConfigureRemoteApiForOAuth failure ({})".format(e))
        click.echo('')
        click.echo("To authenticate run:")
        click.echo("    gcloud auth application-default login")
        return

    os.environ['SERVER_SOFTWARE'] = 'remote_api_shell'


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    generate()
