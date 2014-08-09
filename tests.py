import unittest
import app


class MyTestCase(unittest.TestCase):
    def test_sample(self):
        f = open('fake_message.json', 'r')
        app.consume_posts(None,None,None,f.read())
