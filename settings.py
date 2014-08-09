from os import environ

QUEUE_NAME = 'fb'
RABBITMQ_HOST = "rabbitmq.microhackathon.pl"
RABBITMQ_PORT = 5672

SERVICE_IP = environ.get('SERVICE_IP') or '12.34.56.78'

LOGGING_FILE = environ.get('LOGGING_FILE') or "/home/deployment/logs/facebook-places-analyser.log"
