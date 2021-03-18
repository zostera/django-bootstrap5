from django.test import TestCase

from django_bootstrap5.exceptions import BootstrapError
from tests.base import render_template_with_form


class ButtonTest(TestCase):
    def test_button(self):
        res = render_template_with_form("{% bootstrap_button 'button' size='lg' %}")
        self.assertEqual(res.strip(), '<button class="btn btn-primary btn-lg">button</button>')

        link_button = '<a class="btn btn-primary btn-lg" href="#" role="button">button</a>'

        res = render_template_with_form("{% bootstrap_button 'button' size='lg' href='#' %}")
        self.assertIn(res.strip(), link_button)
        res = render_template_with_form("{% bootstrap_button 'button' button_type='link' size='lg' href='#' %}")
        self.assertIn(res.strip(), link_button)
        with self.assertRaises(BootstrapError):
            res = render_template_with_form("{% bootstrap_button 'button' button_type='button' href='#' %}")
