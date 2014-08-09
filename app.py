#!/usr/bin/env python
import pika
import logging


def consume_posts(ch, method, properties, body):
    print "Consuming posts: {}".format(body)


if __name__ == '__main__':
    logging.info("Initializing app")

    logging.info("Connecting to queue")

    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))

    channel = connection.channel()

    # Make sure the queue exists
    channel.queue_declare(queue='facebook_posts')

    print ' [*] Waiting for messages. To exit press CTRL+C'

    channel.basic_consume(consume_posts, queue='facebook_posts')

    channel.start_consuming()
