"""cosmicpi-protocol - Parser for data read from Arduino."""

import time
from threading import Thread, Timer
try:
    from Queue import Queue
except ImportError:
    from queue import Queue

import pkg_resources
import yaml
from werkzeug.exceptions import NotFound
from werkzeug.routing import Map, Rule

__version__ = '0.1.0'
__author__ = 'Jiri Kuncar <jiri.kuncar@gmail.com>'
__all__ = ('Detector', 'Parser')


def yield_protocols():
    """Yield tuples with protocol name and path."""
    for group in pkg_resources.iter_entry_points('cosmicpi.protocols'):
        yield group.name, pkg_resources.resource_filename(
            group.module_name, '{0}.yaml'.format(group.name)
        )

def load_events():
    """Load defaut events configuration."""
    return yaml.load(pkg_resources.resource_stream(
        'cosmicpi_protocol', 'events.yaml'
    ))

class Parser(object):
    """Parser of messages defined in protocol."""

    def __init__(self, protocols=None):
        """Build protocol parser."""
        self.rules = Map()
        for protocol, path in protocols or yield_protocols():
            with open(path, 'r') as fp:
                for endpoint, rule in yaml.load(fp).get('rules', {}).items():
                    self.rules.add(Rule(
                        '/{0}'.format(rule),
                        endpoint='{0}:{1}'.format(protocol, endpoint),
                    ))
        self.matcher = self.rules.bind('')

    def match(self, message):
        """Match incomming message and return tuple (endpoint, data)."""
        return self.matcher.match(message)


class Detector(object):
    """Detector controller."""

    def __init__(self, events=None, status=None):
        """Create a detector state."""
        self.events = events or load_events()
        self.status = status or {}
        self.queue = Queue()

    def clock(self):
        """Start timers."""
        def worker(period, keys):
            """Define periodic task."""
            while True:
                time.sleep(period)
                event = self.prepare_event(*keys)
                if event:
                    self.queue.put(event)

        for timers in self.events.get('timers', []):
            for period, keys in timers.items():
                t = Thread(target=worker, args=(int(period), keys))
                t.daemon = True
                t.start()


    def prepare_event(self, *keys):
        """Build output from status keys."""
        keys = set(keys)
        return {
            key: value for key, value in self.status.items() if key in keys
        }

    def update(self, identifier, data):
        """Update status with new data for given identifier."""
        protocol, event = identifier.split(':', 1)
        self.status[event] = data
        if event in self.events.get('triggers', {}):
            keys = self.events['triggers'][event]
            self.queue.put(self.prepare_event(*keys))

    def read(self, input_, parser=None):
        """Read and parse input."""
        parser = parser or Parser()

        self.clock()

        for line in input_.readlines():
            if not line:
                break
            try:
                self.update(*parser.match(line.strip()))
            except NotFound:
                pass
                # TODO add logging

        self.queue.join()
