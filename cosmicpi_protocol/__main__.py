"""Command line interface for testing protocols."""

import json
import sys

import click
from werkzeug.exceptions import NotFound

from . import Parser


@click.command()
@click.argument('input_', type=click.File('rb'))
@click.argument('output', type=click.File('wb'))
def cli(input_, output):
    """Parse input file and print JSON output."""
    parser = Parser()
    for line in input_.readlines():
        if line:
            try:
                output.write(json.dumps(parser.match(line.strip())))
                output.write('\n')
            except NotFound:
                click.echo('Could not parse: {0}'.format(line),
                           file=sys.stderr)

            output.flush()


if __name__ == '__main__':  # pragma: no cover
    cli()
