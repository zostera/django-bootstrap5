import logging


from django.test import TestCase

from django_bootstrap5.core import get_bootstrap_setting
import urllib.request



class UrlValidityTestCase(TestCase):
    def test_get_bootstrap_setting(self):
        """ tests that it's possible to pull the URLs listed in the settings

        Reason: https://github.com/zostera/django-bootstrap5/issues/208

        """

        logger = logging.getLogger(__name__)

        jsurl = get_bootstrap_setting("javascript_url")
        cssurl = get_bootstrap_setting("css_url")

        for url in (jsurl.get("url"), cssurl.get("url")):
            req = urllib.request.Request(url=url, method='GET')

            with urllib.request.urlopen(req) as request:
                logger.debug(f"Status for {url}: {request.status}")
                self.assertLess(request.status,400)

