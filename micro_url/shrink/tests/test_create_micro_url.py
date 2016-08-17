import unittest
import urlparse

from django.test import Client
from django.core.urlresolvers import reverse
from django.core.management import call_command

from shrink.models import MicroUrl


class MicroUrlTestCreate(unittest.TestCase):
    """ Tests the create_micro_url view """

    def setUp(self):
        """ Setup client and create fake users """

        self.client = Client()
        call_command('create_fake_users', '3')

    def tearDown(self):
        """ Good bye """

        del self.client

    def __validate(self, response, error):
        """ Validates response status code to be 200,
        containing form error
        """

        self.assertEqual(response.status_code, 200)
        self.assertIn(error, response.content)

    def test_submit_link_and_alias(self):
        """ Enter valid link and alias """

        data = {'link': 'https://wwww.google.com/?search=asma',
                'alias': 'd1234'}
        response = self.client.post('/', data)  # post valid link and alias

        # (302) Redirection upon successful form submission
        self.assertEqual(response.status_code, 302)

        # micro url object created
        micro_url_object = MicroUrl.objects.get_micro_url_object(alias=data['alias'])
        self.assertNotEqual(micro_url_object, None)
 
    def test_submit_link_without_alias(self):
        """ Enter valid link and no alias """

        data = {'link': 'https://wwww.google.com/?search=kothari'}
        response = self.client.post('/', data)  # post valid link and alias

        # (302) Redirection upon successful form submission
        self.assertEqual(response.status_code, 302)

        # micro url object created
        micro_url_object = MicroUrl.objects.get(link=data['link'])
        self.assertNotEqual(micro_url_object, None)
 
    def test_submit_empty_form(self):
        """ Validation Error results in landing back to original page with errors """

        data = {}
        response = self.client.post('/', data)  # Post empty form
 
        # 200 response contains the form error
        error = 'This field is required'
        self.__validate(response, error)

    def test_submit_duplicate_link(self):
        """ Validation Error results in landing back to original page with errors """

        data = {'link': 'https://wwww.google.com/'}
        response = self.client.post('/', data)  # post link
        response = self.client.post('/', data)  # post duplicate link

        # 200 response contains the form error
        error = 'already generated for this url'
        self.__validate(response, error)

    def test_submit_duplicate_alias(self):
        """ Validation Error results in landing back to original page with errors """

        data = {'link': 'https://wwww.google.com/', 'alias': 'abcde'}
        response = self.client.post('/', data)  # post link and alias
        data = {'link': 'https://wwww.google.com?search=asma', 'alias': 'abcde'}
        response = self.client.post('/', data)  # post new link with duplicate alias

        # 200 response contains the form error
        error = 'is already taken'
        self.__validate(response, error)

    def test_submit_alias_with_special_characters(self):
        """ Validation Error results in landing back to original page with errors """

        data = {'link': 'https://wwww.google.com/', 'alias': 'a@b!5'}
        response = self.client.post('/', data)  # post alias with special characters

        # 200 response contains the form error
        error = 'Only alphanumeric characters are allowed'
        self.__validate(response, error)

    def test_submit_smaller_alias(self):
        """ Validation Error results in landing back to original page with errors """

        data = {'link': 'https://wwww.google.com/', 'alias': 'abc'}
        response = self.client.post('/', data)  # post a tiny alias

        # 200 response contains the form error
        error = 'Please provide a custom alias of  atleast'
        self.__validate(response, error)

    def test_submit_invalid_link(self):
        """ Validation Error results in landing back to original page with errors """

        data = {'link': 'ab123', 'alias': 'abcde'}
        response = self.client.post('/', data)  # post an invalid link

        # 200 response contains the form error
        error = 'Enter a valid URL'
        self.__validate(response, error)

    def test_submit_large_alias(self):
        """ Validation Error results in landing back to original page with errors """

        data = {'link': 'https://wwww.google.com/', 'alias': 'abcdefgh'}
        response = self.client.post('/', data)  # post an invalid larger alias

        # 200 response contains the form error
        error = 'Ensure this value has at most 5 characters'
        self.__validate(response, error)

