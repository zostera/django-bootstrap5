from django_bootstrap5.exceptions import BootstrapError

from .base import BootstrapTestCase, TestForm, html_39x27


class FieldTestCase(BootstrapTestCase):
    def test_illegal_field(self):
        with self.assertRaises(BootstrapError):
            self.render("{% bootstrap_field field %}", {"field": "illegal"})

    def test_show_help(self):
        html = self.render("{% bootstrap_field form.subject %}", {"form": TestForm()})
        self.assertIn("my_help_text", html)
        self.assertNotIn("<i>my_help_text</i>", html)
        html = self.render("{% bootstrap_field form.subject show_help=False %}", {"form": TestForm()})
        self.assertNotIn("my_help_text", html)

    def test_placeholder(self):
        html = self.render("{% bootstrap_field form.subject %}", {"form": TestForm()})
        self.assertIn('type="text"', html)
        self.assertIn('placeholder="placeholdertest"', html)

    def test_xss_field(self):
        html = self.render("{% bootstrap_field form.xss_field %}", {"form": TestForm()})
        self.assertIn('type="text"', html)
        self.assertIn(html_39x27(">XSS&quot; onmouseover=&quot;alert(&#x27;Hello, XSS&#x27;)&quot; foo=&quot;<"), html)
        self.assertIn(
            html_39x27('placeholder="XSS&quot; onmouseover=&quot;alert(&#x27;Hello, XSS&#x27;)&quot; foo=&quot;"'), html
        )

    def test_empty_permitted(self):
        """If a form has empty_permitted, no fields should get the CSS class for required."""
        form = TestForm()

        html = self.render("{% bootstrap_field form.subject %}", {"form": form})
        self.assertIn("django_bootstrap5-req", html)

        form.empty_permitted = True
        html = self.render("{% bootstrap_field form.subject %}", {"form": form})
        self.assertNotIn("django_bootstrap5-req", html)

    def test_size(self):
        def _test_size(param, klass):
            html = self.render('{% bootstrap_field form.subject size="' + param + '" %}', {"form": TestForm()})
            self.assertIn(klass, html)

        def _test_size_medium(param):
            html = self.render('{% bootstrap_field form.subject size="' + param + '" %}', {"form": TestForm()})
            self.assertNotIn("form-control-lg", html)
            self.assertNotIn("form-control-sm", html)
            self.assertNotIn("form-control-md", html)

        _test_size("sm", "form-control-sm")
        _test_size("lg", "form-control-lg")
        _test_size_medium("md")
        _test_size_medium("")

    def test_label(self):
        self.assertEqual(
            self.render('{% bootstrap_label "foobar" label_for="subject" %}'),
            '<label for="subject">foobar</label>',
        )
