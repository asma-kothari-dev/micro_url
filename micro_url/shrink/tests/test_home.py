import unittest
from django.test import Client


class MicroUrlTestHome(unittest.TestCase):
    """ Tests the access to home page """

    def setUp(self):
        """ Setup client """

        self.client = Client()

    def tearDown(self):
        """ Good Bye """

        del self.client

    def test_home(self):
        """ Access home page """

        response = self.client.get('/', follow=True)
        self.assertEqual(response.status_code, 200)
