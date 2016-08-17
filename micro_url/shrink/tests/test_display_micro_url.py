import unittest
import urlparse

from django.test import Client
from django.core.urlresolvers import reverse
from django.core.management import call_command

from shrink.models import MicroUrl


class MicroUrlTestDisplay(unittest.TestCase):
    """ Tests the display_micro_url view """

    def setUp(self):
        """ Setup client and create fake users """

        self.client = Client()
        call_command('create_fake_users', '3')
        link = 'https://www.google.com'
        alias = 'abcd5'
        self.micro_url_object = MicroUrl.objects.create(link=link, alias=alias)

    def tearDown(self):
        """ Good bye """

        self.micro_url_object.delete()
        del self.client

    def __context(self, response):
        """ Extract context from response
        :return: <class 'django.template.context.RequestContext'>"""
        
        return response.context[0]

    def test_display_micro_url(self):
        """ Display Micro URL """

        endpoint = reverse('display_micro_url', args=(self.micro_url_object.id,))
        response = self.client.get(endpoint)  # perform GET request

        # response status code 200
        self.assertEqual(response.status_code, 200)

        info = 'Micro URL is generated!'
        self.assertIn(info, response.content)

        micro_url = self.__context(response).get('micro_url', None)
        self.assertEqual(micro_url, self.micro_url_object.micro_url)

    def test_page_not_found(self):
        """ Page Not Found """

        # send a random object ID that is not associated to any mirco url
        endpoint = reverse('display_micro_url', args=(3,))
        response = self.client.get(endpoint)  # perform GET request

        # response status code 404
        self.assertEqual(response.status_code, 404)
        self.assertIn('Page Not Found', response.content)

