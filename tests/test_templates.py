from tests.base import BootstrapTestCase


class TemplateTestCase(BootstrapTestCase):
    def test_empty_template(self):
        self.assertEqual(self.render("").strip(), "")

    def test_text_template(self):
        self.assertEqual(self.render("some text").strip(), "some text")

    def test_bootstrap5_html_template_title(self):
        html = self.render(
            '{% extends "django_bootstrap5/bootstrap5.html" %}{% block bootstrap5_title %}x-title-x{% endblock %}',
            load_bootstrap=False,
        )
        self.assertIn("x-title-x", html)

    def test_bootstrap5_html_template_content(self):
        html = self.render(
            '{% extends "django_bootstrap5/bootstrap5.html" %}{% block bootstrap5_content %}x-content-x{% endblock %}',
            load_bootstrap=False,
        )
        self.assertIn("x-content-x", html)
