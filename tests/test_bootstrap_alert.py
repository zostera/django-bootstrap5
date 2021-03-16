from django.test import TestCase

from .test_templates import render_template_with_bootstrap


class BootstrapAlertTest(TestCase):
    def test_bootstrap_alert(self):
        self.assertEqual(
            render_template_with_bootstrap('{% bootstrap_alert "content" dismissible=False %}'),
            '<div class="alert alert-info" role="alert">content</div>',
        )

    def test_bootstrap_alert_dismissible(self):
        self.assertHTMLEqual(
            render_template_with_bootstrap('{% bootstrap_alert "content" %}'),
            (
                '<div class="alert alert-info alert-dismissible fade show" role="alert">'
                "content"
                '<button aria-label="close" class="btn-close" data-bs-dismiss="alert" type="button">'
                "</div>"
            ),
        )

    def test_bootstrap_alert_html_content(self):
        self.assertEqual(
            render_template_with_bootstrap('{% bootstrap_alert "foo<br>bar" dismissible=False %}'),
            '<div class="alert alert-info" role="alert">foo<br>bar</div>',
        )
        self.assertEqual(
            render_template_with_bootstrap(
                "{% bootstrap_alert value dismissible=False %}", context={"value": "foo<br>bar"}
            ),
            '<div class="alert alert-info" role="alert">foo&lt;br&gt;bar</div>',
        )
        self.assertEqual(
            render_template_with_bootstrap(
                "{% bootstrap_alert value|safe dismissible=False %}", context={"value": "foo<br>bar"}
            ),
            '<div class="alert alert-info" role="alert">foo<br>bar</div>',
        )
