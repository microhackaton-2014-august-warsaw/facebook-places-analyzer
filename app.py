#!/usr/bin/env python
import logging
import json

from os import environ
import pika

QUEUE_NAME = 'facebook_posts'
RABBITMQ_HOST = environ.get('RABBITMQ_HOST') or 'localhost'
RABBITMQ_PORT = environ.get('RABBITMQ_PORT') or 5672


def consume_posts(ch, method, properties, body):
    logging.info('Consuming posts...')
    try:
        data = json.loads(body)
        profileLocation = data["hometown"]["location"]
        profileHometown = data["location"]["location"]
        locationPost0 = data["posts"][0]["place"]["location"]
        print "Consuming posts: {}".format(data)
    except Exception, e:
        print(e)
        logging.info(e)


if __name__ == '__main__':
    logging.info("Initializing app")

    logging.info("Connecting to queue")

    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST, port=RABBITMQ_PORT))

    channel = connection.channel()

    # Make sure the queue exists
    channel.queue_declare(queue=QUEUE_NAME)

    print ' [*] Waiting for messages. To exit press CTRL+C'

    channel.basic_consume(consume_posts, queue='facebook_posts')

    channel.start_consuming()
