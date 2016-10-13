"""Command line interface for testing protocols."""

import json
import sys

import click
from werkzeug.exceptions import NotFound

from . import Detector, Parser


@click.group()
def cli():
    """Command line interface for testing CosmicPi."""


@cli.command()
@click.argument('input_', type=click.File('rb'), default='-')
@click.argument('output', type=click.File('wb'), default='-')
def parse(input_, output):
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


@cli.command()
@click.argument('input_', type=click.File('rb'), default='-')
@click.argument('output', type=click.File('wb'), default='-')
def run(input_, output):
    """Run simple event agregator."""
    from threading import Thread, Timer

    detector = Detector()

    def worker():
        while True:
            item = detector.queue.get()
            output.write(json.dumps(item))
            output.write('\n')
            output.flush()
            detector.queue.task_done()

    number_worker_threads = 1
    for i in range(number_worker_threads):
        t = Thread(target=worker)
        t.daemon = True
        t.start()

    detector.read(input_)


if __name__ == '__main__':  # pragma: no cover
    cli()
