import requests
import json
import app


def post_localizations(json_body):
    facebook_correlator_url = '{}/api/{}'.format(app.facebook_correlator_url, json_body["pair_id"])
    requests.post(facebook_correlator_url, data=json.dumps(json_body))
