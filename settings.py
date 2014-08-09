from os import environ

QUEUE_NAME = 'facebook_posts'
RABBITMQ_HOST = environ.get('RABBITMQ_HOST') or 'localhost'
RABBITMQ_PORT = environ.get('RABBITMQ_PORT') or 5672

SERVICE_IP = environ.get('SERVICE_IP') or '12.34.56.78'

LOGGING_FILE = environ.get('LOGGING_FILE') or '/tmp/log'
