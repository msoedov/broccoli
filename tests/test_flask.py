import unittest
from .fixtures.flask_app import web_app, hello_world


class TestPlugin(unittest.TestCase):

    def test_plugin(self):
        # Use Flask's test client for our test.
        app = web_app()
        test_app = app.test_client()

        response = test_app.get('/')

        # Assert response is 200 OK.
        self.assertEquals(response.status, "200 OK")
        self.assertEquals(response.data, b"Hello World! foo")

    def test_without_client(self):
        web_app()
        val = hello_world()
        self.assertEqual(val, "Hello World! foo")

    def test_with_mocked_value(self):
        web_app()

        class Mock(object):
            arg = 'bar'

        val = hello_world(Mock())
        self.assertEqual(val, "Hello World! bar")
