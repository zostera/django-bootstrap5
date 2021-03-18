from django.test import TestCase

from tests.base import render_template, render_template_with_form


class TemplateTest(TestCase):
    def test_empty_template(self):
        res = render_template_with_form("")
        self.assertEqual(res.strip(), "")

    def test_text_template(self):
        res = render_template_with_form("some text")
        self.assertEqual(res.strip(), "some text")

    def test_bootstrap5_html_template_title(self):
        res = render_template(
            '{% extends "django_bootstrap5/bootstrap5.html" %}'
            + "{% block bootstrap5_title %}"
            + "test_bootstrap5_title"
            + "{% endblock %}"
        )
        self.assertIn("test_bootstrap5_title", res)

    def test_bootstrap5_html_template_content(self):
        res = render_template(
            '{% extends "django_bootstrap5/bootstrap5.html" %}'
            + "{% block bootstrap5_content %}"
            + "test_bootstrap5_content"
            + "{% endblock %}"
        )
        self.assertIn("test_bootstrap5_content", res)
