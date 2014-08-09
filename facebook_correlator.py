import requests
import json

def post_localizations(json_body):
    requests.post('...', data=json.dumps(json_body))
