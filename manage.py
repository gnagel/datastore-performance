from __future__ import absolute_import

import click
from jinja2 import Template


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


if __name__ == "__main__":
    generate()
