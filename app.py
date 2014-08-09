#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import json
import latlontool

import pika
import facebook_correlator
import settings

from service_discovery import ServiceDiscovery


def place_data(location):
    return latlontool.place_data(location["latitude"], location["longitude"])


def place_with_probability(place):
    place_extended = dict()
    place_extended["place"] = place
    place_extended["origin"] = "facebook"
    return place_extended


def prepare_json_output(data):
    profileLocation = data["profile"]["hometown"]["location"]
    profileHometown = data["profile"]["location"]["location"]
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
    output["corelationId"] = data["corelationId"]
    output["pairId"] = data["pairId"]
    output["places"] = places
    return output

def consume_posts(ch, method, properties, body):
    try:
        data = json.loads(body)

        output = prepare_json_output(data)
        facebook_correlator.post_localizations(output)
        print "Consuming posts: {}".format(data)
    except Exception, e:
        print(e)
        logging.info(e)


if __name__ == '__main__':

    logging.basicConfig(
        filename=settings.LOGGING_FILE,
        level=logging.INFO,
        format=u"%(asctime)s.%(msecs).03d+0200 | %(levelname)s | | walSięGościu | | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    logging.info("Initializing app")

    logging.info("Connecting to queue")

    sd = ServiceDiscovery('/pl/pl/microhackaton', 'zookeeper.microhackathon.pl:2181')

    try:
        queue_host = sd.get_instance('rabitmq')
    except:
        queue_host = settings.RABBITMQ_HOST

    try:
        facebook_correlator_url = sd.get_instance('common-places-correlator')
    except:
        facebook_correlator_url = 'private-2876e-microservice1.apiary-mock.com'

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=queue_host, port=settings.RABBITMQ_PORT)
    )

    channel = connection.channel()

    # Make sure the queue exists
    channel.queue_declare(queue=settings.QUEUE_NAME)

    print ' [*] Waiting for messages. To exit press CTRL+C'

    channel.basic_consume(consume_posts, queue='facebook_posts')

    channel.start_consuming()
