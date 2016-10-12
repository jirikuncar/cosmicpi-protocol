"""cosmicpi-protocol - Parser for data read from Arduino."""

import pkg_resources
import yaml
from werkzeug.routing import Map, Rule

__version__ = '0.1.0'
__author__ = 'Jiri Kuncar <jiri.kuncar@gmail.com>'
__all__ = ()


def yield_protocols():
    """Yield tuples with protocol name and path."""
    for group in pkg_resources.iter_entry_points('cosmicpi.protocols'):
        yield group.name, pkg_resources.resource_filename(
            group.module_name, '{0}.yaml'.format(group.name)
        )

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
