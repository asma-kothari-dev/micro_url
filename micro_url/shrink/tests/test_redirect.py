import unittest
import urlparse

from django.http import Http404
from django.test import RequestFactory
from django.core.urlresolvers import reverse
from django.core.management import call_command

from shrink.models import MicroUrl
from shrink.views import redirect


class MicroUrlTestRedirect(unittest.TestCase):
    """ Tests the redirect view """

    def setUp(self):
        """ Setup client and create fake users """

        self.factory = RequestFactory()
        call_command('create_fake_users', '3')
        link = 'https://www.google.com/?search=a55d'
        alias = 'a555c'
        self.micro_url_object = MicroUrl.objects.create(link=link, alias=alias)

    def tearDown(self):
        """ Good bye """

        self.micro_url_object.delete()
        del self.factory

    def test_redirect(self):
        """ Redirect to Original URL """

        endpoint = reverse('redirect')
        request = self.factory.get(endpoint)
        request.META['PATH_INFO'] = '/%s' % self.micro_url_object.alias

        # get response for the custom request
        response = redirect(request)

        # Response: Redirection to original url
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, self.micro_url_object.link)

    def test_redirect_with_trailing_slash(self):
        """ Redirect to Original URL """

        endpoint = reverse('redirect')
        request = self.factory.get(endpoint)
        request.META['PATH_INFO'] = '/%s/' % self.micro_url_object.alias

        # get response for the custom request
        response = redirect(request)

        # Response: Redirection to original url
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, self.micro_url_object.link)

    def test_redirect_with_invalid_alias(self):
        """ Page Not Found """

        endpoint = reverse('redirect')
        request = self.factory.get(endpoint)
        invalid_alias = 'bbbb6'
        request.META['PATH_INFO'] = '/%s/' % invalid_alias

        try:
            response = redirect(request)
        except Exception, exp:
            self.assertEqual(type(exp), Http404)
