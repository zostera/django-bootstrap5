from django.conf import settings

from .base import BootstrapTestCase


class BootstrapAlertTestCase(BootstrapTestCase):
    def test_bootstrap_alert(self):
        self.assertEqual(
            self.render('{% bootstrap_alert "content" dismissible=False %}'),
            '<div class="alert alert-info" role="alert">content</div>',
        )

    def test_bootstrap_alert_type_invalid(self):
        with self.assertRaises(ValueError):
            self.render('{% bootstrap_alert "content" alert_type="nope" %}')

    def test_bootstrap_alert_dismissible(self):
        self.assertEqual(
            self.render('{% bootstrap_alert "content" %}'),
            (
                '<div class="alert alert-info alert-dismissible fade show" role="alert">'
                "content"
                '<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>'
                "</div>"
            ),
        )

    def test_bootstrap_alert_html_content(self):
        self.assertEqual(
            self.render('{% bootstrap_alert "foo<br>bar" dismissible=False %}'),
            '<div class="alert alert-info" role="alert">foo<br>bar</div>',
        )
        self.assertEqual(
            self.render("{% bootstrap_alert value dismissible=False %}", context={"value": "foo<br>bar"}),
            '<div class="alert alert-info" role="alert">foo&lt;br&gt;bar</div>',
        )
        self.assertEqual(
            self.render("{% bootstrap_alert value|safe dismissible=False %}", context={"value": "foo<br>bar"}),
            '<div class="alert alert-info" role="alert">foo<br>bar</div>',
        )
        
        bootstrap = settings.BOOTSTRAP5
        bootstrap["alert-extra-classes"] = ["extra-class"]
        with self.settings(BOOTSTRAP5=bootstrap):
            self.assertEqual(
                self.render('{% bootstrap_alert "foo<br>bar" dismissible=False %}'),
                '<div class="alert alert-info extra-class" role="alert">foo<br>bar</div>',
            )
