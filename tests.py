import unittest
import app


class MyTestCase(unittest.TestCase):
    def test_sample(self):
        app.consume_posts(None,None,None,)
