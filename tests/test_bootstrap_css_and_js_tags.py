from django.test import TestCase

from django_bootstrap5.core import get_bootstrap_setting
from tests.base import TestForm, render_template_with_form


class MediaTest(TestCase):
    def expected_css(self, tag):
        template = '<link href="{url}" integrity="{integrity}" crossorigin="{crossorigin}" rel="stylesheet">'
        setting = get_bootstrap_setting(tag + "_url")
        return template.format(**setting)

    def expected_js(self, tag):
        template = '<script src="{url}" integrity="{integrity}" crossorigin="{crossorigin}"></script>'
        setting = get_bootstrap_setting(tag + "_url")
        return template.format(**setting)

    def test_bootstrap_javascript_tag(self):
        html = render_template_with_form("{% bootstrap_javascript %}")
        # Bootstrap
        self.assertInHTML(self.expected_js("javascript"), html)

    def test_bootstrap_css_tag(self):
        html = render_template_with_form("{% bootstrap_css %}").strip()
        self.assertInHTML(self.expected_css("css"), html)
        # Theme
        self.assertInHTML('<link rel="stylesheet" href="//example.com/theme.css">', html)

    def test_bootstrap_setting_filter(self):
        res = render_template_with_form('{{ "required_css_class"|bootstrap_setting }}')
        self.assertEqual(res.strip(), "django_bootstrap5-req")
        res = render_template_with_form('{% if "javascript_in_head"|bootstrap_setting %}head{% else %}body{% endif %}')
        self.assertEqual(res.strip(), "head")

    def test_bootstrap_required_class(self):
        form = TestForm()
        res = render_template_with_form("{% bootstrap_form form %}", {"form": form})
        self.assertIn("django_bootstrap5-req", res)

    def test_bootstrap_error_class(self):
        form = TestForm({})
        res = render_template_with_form("{% bootstrap_form form %}", {"form": form})
        self.assertIn("django_bootstrap5-err", res)

    def test_bootstrap_bound_class(self):
        form = TestForm({"sender": "sender"})
        res = render_template_with_form("{% bootstrap_form form %}", {"form": form})
        self.assertIn("django_bootstrap5-bound", res)


class JavaScriptTagTest(TestCase):
    def test_bootstrap_javascript(self):
        res = render_template_with_form("{% bootstrap_javascript %}")
        self.assertIn("bootstrap", res)
