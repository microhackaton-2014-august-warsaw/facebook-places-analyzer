#!/usr/bin/env python
from latlontool import place_data
import pika
import logging


def consume_posts(ch, method, properties, body):
    print "Consuming posts: {}".format(body)


if __name__ == '__main__':
    logging.info("Initializing app")

    print (place_data(52.203226263818, 21.0467223005))
    print (place_data(49.418874, 7.321701))
    print (place_data(48.135125, 11.581981))
    print (place_data(37.774929, -122.419416))

    logging.info("Connecting to queue")

    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))

    channel = connection.channel()

    # Make sure the queue exists
    channel.queue_declare(queue='facebook_posts')

    print ' [*] Waiting for messages. To exit press CTRL+C'

    channel.basic_consume(consume_posts, queue='facebook_posts')

    channel.start_consuming()
