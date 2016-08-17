import unittest
import urlparse

from django.test import Client
from django.core.urlresolvers import reverse
from django.core.management import call_command

from shrink.models import MicroUrl


class MicroUrlTestPreview(unittest.TestCase):
    """ Tests the preview_micro_url view """

    def setUp(self):
        """ Setup client and create fake users """

        self.client = Client()
        call_command('create_fake_users', '3')
        link = 'https://www.google.com'
        alias = 'a555c'
        self.micro_url_object = MicroUrl.objects.create(link=link, alias=alias)

    def tearDown(self):
        """ Good bye """

        self.micro_url_object.delete()
        del self.client

    def __context(self, response):
        """ Extract context from response
        :return: <class 'django.template.context.RequestContext'>"""
        
        return response.context[0]

    def test_preview_micro_url(self):
        """ Preview Micro URL """

        endpoint = reverse('preview_micro_url', args=(self.micro_url_object.id,))
        response = self.client.get(endpoint)  # perform GET request

        # response status code 200
        self.assertEqual(response.status_code, 200)

        info = 'Preview Micro URL'
        self.assertIn(info, response.content)

        micro_url = self.__context(response).get('micro_url', None)
        self.assertEqual(micro_url, self.micro_url_object.micro_url)

        original_url = self.__context(response).get('original_url', None)
        self.assertEqual(original_url, self.micro_url_object.link)

    def test_page_not_found(self):
        """ Page Not Found """

        # send a random object ID that is not associated to any mirco url
        random_id = 300

        endpoint = reverse('preview_micro_url', args=(random_id,))
        response = self.client.get(endpoint)  # perform GET request

        # response status code 404
        self.assertEqual(response.status_code, 404)
        self.assertIn('Page Not Found', response.content)


