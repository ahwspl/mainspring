from mainspring.server.helpers.rabbit.pika_client import PikaClient
import logging
import json

logger = logging.getLogger(__name__)


class PikaPublisher(PikaClient):
    """
    Class used for publishing messages to message bus

    Attributes
    ----------
    dl_queue: str
        name of the deadletter queue
    exchange: str
        name of the exchange that we want to publish to
    queue: str
        name of the response queue
    queue_ttl: int
        time to live for messages in response queue before they are moved to deadletter queue
    """
    def __init__(self, io_loop):
        super().__init__(io_loop)

    def on_queue_declare_ok(self, method_frame):
        """
        callback function that is called when a queue is created for first time or is identified that it exists

        Parameters
        ----------
        method_frame
            Method frame associated with the created queue

        """
        logger.info('RabbitMQ queue - {} exists or created'.format(self.queue))

    def on_channel_open(self, channel):
        """
        callback function that is called when an RMQ channel is opened

        Parameters
        ----------
        channel
            a reference to the channel object that is opened

        """
        logger.info('RabbitMQ publisher channel opened')
        self.channel = channel
        self.channel.add_on_close_callback(self.on_channel_closed)

    def publish(self, msg, queue, properties=None):
        """
        function that publishes a message to response queue on message bus

        Parameters
        ----------
        msg: dict
            dictionary containing the message that we want to publish to message bus
        queue: str
        properties: dict

        """
        if self.channel is None:
            self.connect()

        logger.info("publishing to message bus: \n{}".format(json.dumps(msg, indent=4)))
        msg_bytes = json.dumps(msg).encode('UTF-8')
        self.channel.basic_publish(exchange=self.exchange, routing_key=self.queue, body=msg_bytes, mandatory=True)



