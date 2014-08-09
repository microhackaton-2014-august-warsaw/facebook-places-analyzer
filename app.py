#!/usr/bin/env python
import logging
import json
import latlontool

from os import environ
import pika
import facebook_correlator

QUEUE_NAME = 'facebook_posts'
RABBITMQ_HOST = environ.get('RABBITMQ_HOST') or 'localhost'
RABBITMQ_PORT = environ.get('RABBITMQ_PORT') or 5672


def place_data(location):
    return latlontool.place_data(location["latitude"], location["longitude"])

def place_with_probability(place):
    place_extended = dict()
    place_extended["place"] = place
    place_extended["probability"] = "high"
    place_extended["origin"] = "facebook"
    return place_extended

def consume_posts(ch, method, properties, body):
    try:
        data = json.loads(body)
        profileLocation = data["hometown"]["location"]
        profileHometown = data["location"]["location"]
        places = list()
        profileLocationCode = place_data(profileLocation)
        places.append(place_with_probability(profileLocationCode))
        profileHometownCode = place_data(profileHometown)
        places.append(place_with_probability(profileHometownCode))
        posts = data["posts"]
        for post in posts:
            print post["created_time"]
            if "place" in post:
                location = post["place"]["location"]
                code = place_data(location)
                places.append(place_with_probability(code))
                print post["place"]["location"]
        output = dict()
        output["places"] = places
        facebook_correlator.post_localizations(output)
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
    channel.queue_declare(queue='facebook_posts')

    print ' [*] Waiting for messages. To exit press CTRL+C'

    channel.basic_consume(consume_posts, queue='facebook_posts')

    channel.start_consuming()
