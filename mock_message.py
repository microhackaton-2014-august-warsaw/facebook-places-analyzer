#!/usr/bin/env python
from os import environ
import pika

QUEUE_NAME = 'facebook_posts'
RABBITMQ_HOST = environ.get('RABBITMQ_HOST') or 'localhost'
RABBITMQ_PORT = environ.get('RABBITMQ_PORT') or 5672

connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST, port=RABBITMQ_PORT))
channel = connection.channel()

channel.queue_declare(queue=QUEUE_NAME)

json_string = open('fake_message.json', 'r').read()
channel.basic_publish(exchange='', routing_key=QUEUE_NAME, body=json_string)

print " [x] Sent 'Hello World!'"

connection.close()
