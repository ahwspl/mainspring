"""A job to send rabbitmq message periodically."""

import pika
import logging
import json
import uuid
from mainspring import job
import os
from mainspring import settings
from pika.adapters import tornado_connection
import tornado.ioloop
from pika.exceptions import AMQPConnectionError, AuthenticationError, ProbableAuthenticationError
from mainspring.server.helpers.rabbit.pika_client import PikaClient

logger = logging.getLogger(__name__)


class RabbitJob(job.JobBase):

    MAX_RETRIES = 3
    TIMEOUT = 10

    @classmethod
    def meta_info(cls):
        return {
            'job_class_string': '%s.%s' % (cls.__module__, cls.__name__),
            'notes': ('This sends message to a RabbitMq channel. To run this job, you have to run '
                      'scheduler with environment variable RABBIT_CONFIG_DICT'),
            'arguments': [
                # exchange
                {
                    'type': 'string',
                    'description': 'What exchange you want the message to be routed from'
                },

                # channel
                {
                    'type': 'string',
                    'description': 'What channel you want to send the message to'
                },

                # message
                {
                    'type': 'string',
                    'description': 'Message object to be sent\n'
                                   '{"type": "TRIGGER_EVENT_NAME", "body": {"key": "value"}}'
                },

                # properties
                {
                    'type': 'string', 'description': 'Additional properties.'},
            ],
            'example_arguments': (
                '["exchange-name", "queue-name", "{\"type\": \"datasync\"}", "{\"reply_to\": \"reply-queue\"}"]'
            )
        }

    def run(self, exchange, queue, message, properties=None, *args, **kwargs):

        try:
            # This URL looks like this:
            # http://hooks.slack.com/services/T024TTTTT/BBB72BBL/AZAAA9u0pA4ad666eMgbi555
            # (not a real api url, don't try it :)
            #
            # You can get this url by adding an incoming webhook:
            rabbit = settings.RABBIT_CONFIG_DICT
            host = rabbit['host']
            message = json.loads(message)
            properties = json.loads(properties) if properties is not None else None
        except KeyError:
            logger.error('Environment variable RABBIT_CONFIG_DICT is not specified. '
                         'So we cannot send rabbit message.')
            raise KeyError('You have to set Environment variable RABBIT_CONFIG_DICT first.')
        else:
            logger.info("Establishing connection with RMQ server and publishing message basis presence of propeeties")
            io_loop = tornado.ioloop.IOLoop.current()
            rmq_client = PikaClient(io_loop=io_loop)
            rmq_client.connect()

            message_bytes = json.dumps(message).encode('utf-8')
            if properties and 'reply_to' in properties.keys():
                rmq_client.channel.basic_publish(
                    exchange=exchange, routing_key=queue, body=message_bytes,
                    properties=pika.BasicProperties(
                        delivery_mode=2,  # make message persistent
                        reply_to=properties['reply_to'],
                        correlation_id=str(uuid.uuid4()),
                        content_type='application/json',
                        headers={"key": "value"}
                    )
                )
            else:
                rmq_client.channel.basic_publish(
                    exchange=exchange, routing_key=queue, body=message_bytes,
                    properties=pika.BasicProperties(
                        delivery_mode=2,  # make message persistent
                        correlation_id=str(uuid.uuid4()),
                        content_type='application/json',
                        headers={"key": "value"}
                    )
                )

            rmq_client.close_connection()
            logger.info("Rabbit-MQ connection has been closed after successfully publishing the message!")


if __name__ == "__main__":
    # You can easily test this job here
    job = RabbitJob.create_test_instance()
    job.run(
        exchange='mainspring-exchange',
        queue='mainspring-requests',
        message="{\"type\": \"GSUITE_SHARE_CALENDAR\",\"body\":{\"time_period\":\"86400\"}}"
    )
