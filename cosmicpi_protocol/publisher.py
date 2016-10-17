"""Publish event via AMQP."""

import json

import pika


class Publisher(object):
    """Publish events."""

    def __init__(self, broker):
        """Create new connection and channel."""
        self.connection = pika.BlockingConnection(
            pika.URLParameters(broker)
        )
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange='events', type='fanout')
        self.properties = pika.BasicProperties(
            content_type='application/json'
        )

    def publish(self, data):
        """Publish an event."""
        self.channel.basic_publish(
            exchange='events',
            routing_key='',
            body=json.dumps(data),
            properties=self.properties,
        )

    def close(self):
        """Close AMQP connection."""
        self.connection.close()
