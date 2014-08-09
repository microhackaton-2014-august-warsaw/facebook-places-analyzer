#!/usr/bin/env python
import pika
import logging
import urllib2

def hello_world(request):
    return Response('Hello %(name)s!' % request.matchdict)

def consume_posts(ch, method, properties, body):
    print "Consuming posts: {}".format(body)



def test_lat_lon_to_country_code():
    print(urllib2.urlopen('http://api.geonames.org/countryCode?lat=52.203226263818&lng=21.0467223005&username=a273719').read())


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
