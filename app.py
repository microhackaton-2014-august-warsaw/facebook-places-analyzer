#!/usr/bin/env python
from latlontool import place_data
import pika
import logging
import urllib2
import json

def consume_posts(ch, method, properties, body):
    data = json.loads(body)
    profileLocation = data["hometown"]["location"]
    profileHometown = data["location"]["location"]
    locationPost0 = data["posts"][0]["place"]["location"]
    print "Consuming posts: {}".format(data)


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
