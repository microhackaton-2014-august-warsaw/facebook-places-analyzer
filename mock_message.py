#!/usr/bin/env python
import pika
import settings

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=settings.RABBITMQ_HOST, port=settings.RABBITMQ_PORT)
)
channel = connection.channel()

channel.queue_declare(queue=settings.QUEUE_NAME)

json_string = open('fake_message.json', 'r').read()
channel.basic_publish(exchange='', routing_key=settings.QUEUE_NAME, body=json_string)

print " [x] Sent 'Hello World!'"

connection.close()
