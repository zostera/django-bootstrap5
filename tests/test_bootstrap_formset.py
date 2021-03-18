from django.test import TestCase

from django_bootstrap5.exceptions import BootstrapError
from tests.base import render_formset


class BootstrapFormSetTest(TestCase):
    def test_illegal_formset(self):
        with self.assertRaises(BootstrapError):
            render_formset(formset="illegal")
