import logging
import unittest
from dingus import patch
import app
import latlontool
import facebook_correlator
import json

class MyTestCase(unittest.TestCase):
    def test_sample(self):
        f = open('fake_message.json', 'r')
        app.consume_posts(None,None,None,f.read())

    def test_prepare_json_output(self):
        f = open('fake_message.json', 'r')
        data = json.loads(f.read())
        output = app.prepare_json_output(data)
        assert len(output["places"]) == 3
        assert output["corelationId"] == '1'
        assert output["pairId"] == '1'

    def test_latlon_to_city(self):
        asserts = {
            (52.203226263818, 21.0467223005): {'name': u'Warszawa', 'country_code': u'PL'},
            (49.418874, 7.321701): {'name': u'Dunzweiler', 'country_code': u'DE'},
            (48.135125, 11.581981): {'name': u'M\xfcnchen', 'country_code': u'DE'},
            (37.774929, -122.419416): {'name': u'San Francisco', 'country_code': u'US'},
        }

        for latlon in asserts:
            self.assertEqual(latlontool.place_data(*latlon), asserts[latlon])

    def test_posting_to_correlator(self):
        pass


@patch('facebook_correlator.requests')
def tests_aaa():

    print("facebook_correlator.requests.call[0]\n")
    facebook_correlator.post_localizations('test')

    
    assert len(facebook_correlator.requests.calls) == 1
