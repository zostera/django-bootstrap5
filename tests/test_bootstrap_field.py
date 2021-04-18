from django import forms
from django.core.files.uploadedfile import SimpleUploadedFile
from django.forms import TextInput
from django.test import TestCase

from django_bootstrap5.exceptions import BootstrapError

from .base import (
    TestForm,
    html_39x27,
    render_field,
    render_form_field,
    render_template_with_bootstrap,
    render_template_with_form,
)


class BootstrapFieldTest(TestCase):
    def test_input_type_text(self):
        """Test field with text widget."""

        class TestForm(forms.Form):
            test = forms.CharField()

        test_form = TestForm()
        html = render_template_with_bootstrap("{% bootstrap_field form.test %}", context={"form": test_form})
        self.assertHTMLEqual(
            html,
            (
                '<div class="django_bootstrap5-req mb-3">'
                '<label for="id_test" class="form-label">Test</label>'
                '<input class="form-control" id="id_test" name="test" placeholder="Test" required type="text">'
                "</div>"
            ),
        )

    def test_input_type_color(self):
        """Test field with text widget."""

        class TestForm(forms.Form):
            test = forms.CharField(widget=TextInput(attrs={"type": "color"}))

        test_form = TestForm()
        html = render_template_with_bootstrap("{% bootstrap_field form.test %}", context={"form": test_form})
        self.assertHTMLEqual(
            html,
            (
                '<div class="django_bootstrap5-req mb-3">'
                '<label for="id_test" class="form-label">Test</label>'
                '<input class="form-control form-control-color" '
                'id="id_test" name="test" placeholder="Test" required type="color">'
                "</div>"
            ),
        )

    def test_input_type_checkbox(self):
        """Test field with text widget."""

        class TestForm(forms.Form):
            test = forms.BooleanField()

        test_form = TestForm()
        html = render_template_with_bootstrap("{% bootstrap_field form.test %}", context={"form": test_form})
        self.assertHTMLEqual(
            html,
            (
                '<div class="django_bootstrap5-req mb-3">'
                '<div class="form-check">'
                '<input class="form-check-input" id="id_test" name="test" required type="checkbox">'
                '<label class="form-check-label" for="id_test">'
                "Test"
                "</label>"
            ),
        )

    def test_input_type_checkbox_style_switch(self):
        """Test field with text widget."""

        class TestForm(forms.Form):
            test = forms.BooleanField()

        test_form = TestForm()
        html = render_template_with_bootstrap(
            '{% bootstrap_field form.test checkbox_style="switch" %}', context={"form": test_form}
        )
        self.assertHTMLEqual(
            html,
            (
                '<div class="django_bootstrap5-req mb-3">'
                '<div class="form-check form-switch">'
                '<input class="form-check-input" id="id_test" name="test" required type="checkbox">'
                '<label class="form-check-label" for="id_test">'
                "Test"
                "</label>"
            ),
        )

    def test_input_type_text_floating(self):
        """Test field with text widget in floating layout."""

        class TestForm(forms.Form):
            test = forms.BooleanField()

        test_form = TestForm()
        html = render_template_with_bootstrap("{% bootstrap_field form.test %}", context={"form": test_form})
        self.assertHTMLEqual(
            html,
            (
                '<div class="django_bootstrap5-req mb-3">'
                '<div class="form-check">'
                '<input class="form-check-input" id="id_test" name="test" required type="checkbox">'
                '<label class="form-check-label" for="id_test">'
                "Test"
                "</label>"
            ),
        )

    def test_textarea(self):
        """Test field with textarea widget."""

        class TestForm(forms.Form):
            test = forms.CharField(widget=forms.Textarea)

        test_form = TestForm()
        html = render_template_with_bootstrap("{% bootstrap_field form.test %}", context={"form": test_form})
        self.assertHTMLEqual(
            html,
            (
                '<div class="django_bootstrap5-req mb-3">'
                '<label for="id_test" class="form-label">Test</label>'
                '<textarea class="form-control" cols="40" id="id_test" name="test" placeholder="Test"'
                ' required rows="10"></textarea>'
                "</div>"
            ),
        )

    def test_textarea_floating(self):
        """Test field with textarea widget and floating label."""

        class TestForm(forms.Form):
            test = forms.CharField(widget=forms.Textarea)

        test_form = TestForm()
        html = render_template_with_bootstrap(
            '{% bootstrap_field form.test layout="floating" %}', context={"form": test_form}
        )
        self.assertHTMLEqual(
            html,
            (
                '<div class="django_bootstrap5-req form-floating mb-3">'
                '<textarea class="form-control" cols="40" id="id_test" name="test" placeholder="Test"'
                ' required rows="10"></textarea>'
                '<label for="id_test" class="form-label">Test</label>'
                "</div>"
            ),
        )

    def test_input_type_file(self):
        class TestForm(forms.Form):
            test = forms.FileField()

        test_form = TestForm()
        html = render_template_with_bootstrap("{% bootstrap_field form.test %}", context={"form": test_form})
        self.assertHTMLEqual(
            html,
            (
                '<div class="django_bootstrap5-req mb-3">'
                '<label for="id_test" class="form-label">Test</label>'
                '<input class="form-control" id="id_test" name="test" required type="file">'
                "</div>"
            ),
        )

    def test_clearable_file_input(self):
        class TestForm(forms.Form):
            test = forms.FileField(widget=forms.ClearableFileInput, required=False)

        test_form = TestForm()
        self.assertHTMLEqual(
            render_template_with_bootstrap("{% bootstrap_field form.test %}", context={"form": test_form}),
            (
                '<div class="mb-3">'
                '<label for="id_test" class="form-label">Test</label>'
                '<input class="form-control" id="id_test" name="test" type="file">'
                "</div>"
            ),
        )

    def test_clearable_file_input_post(self):
        class TestForm(forms.Form):
            test = forms.FileField(widget=forms.ClearableFileInput, required=False)

        test_form = TestForm({}, {"test": SimpleUploadedFile("test.txt", b"test")})
        self.assertHTMLEqual(
            render_template_with_bootstrap("{% bootstrap_field form.test %}", context={"form": test_form}),
            (
                '<div class="django_bootstrap5-bound mb-3">'
                '<label class="form-label" for="id_test">Test</label>'
                '<input type="file" name="test" class="form-control django_bootstrap5-bound" id="id_test">'
                "</div>"
            ),
        )


class FieldTest(TestCase):
    def _select_one_element(self, html, selector, err_msg):
        """
        Select exactly one html element in an BeautifulSoup html fragment.

        Fail if there is not exactly one element.
        """
        lst = html.select(selector)
        self.assertEqual(len(lst), 1, err_msg)
        return lst[0]

    def test_illegal_field(self):
        with self.assertRaises(BootstrapError):
            render_field(field="illegal")

    def test_show_help(self):
        html = render_form_field("subject")
        self.assertIn("my_help_text", html)
        self.assertNotIn("<i>my_help_text</i>", html)
        html = render_template_with_form("{% bootstrap_field form.subject show_help=0 %}")
        self.assertNotIn("my_help_text", html)

    def test_subject(self):
        res = render_form_field("subject")
        self.assertIn('type="text"', res)
        self.assertIn('placeholder="placeholdertest"', res)

    def test_xss_field(self):
        html = render_form_field("xss_field")
        self.assertIn('type="text"', html)
        self.assertIn(html_39x27(">XSS&quot; onmouseover=&quot;alert(&#x27;Hello, XSS&#x27;)&quot; foo=&quot;<"), html)
        self.assertIn(
            html_39x27('placeholder="XSS&quot; onmouseover=&quot;alert(&#x27;Hello, XSS&#x27;)&quot; foo=&quot;"'), html
        )

    def test_password(self):
        res = render_form_field("password")
        self.assertIn('type="password"', res)
        self.assertIn('placeholder="Password"', res)

    def test_required_field(self):
        required_css_class = "django_bootstrap5-req"
        required_field = render_form_field("subject")
        self.assertIn(required_css_class, required_field)
        not_required_field = render_form_field("message")
        self.assertNotIn(required_css_class, not_required_field)
        # Required settings in field
        form_field = "form.subject"
        rendered = render_template_with_form(
            "{% bootstrap_field " + form_field + ' required_css_class="test-required" %}'
        )
        self.assertIn("test-required", rendered)

    def test_empty_permitted(self):
        """If a form has empty_permitted, no fields should get the CSS class for required."""
        required_css_class = "django_bootstrap5-req"
        form = TestForm()
        res = render_form_field("subject", {"form": form})
        self.assertIn(required_css_class, res)
        form.empty_permitted = True
        res = render_form_field("subject", {"form": form})
        self.assertNotIn(required_css_class, res)

    def test_size(self):
        def _test_size(param, klass):
            res = render_template_with_form('{% bootstrap_field form.subject size="' + param + '" %}')
            self.assertIn(klass, res)

        def _test_size_medium(param):
            res = render_template_with_form('{% bootstrap_field form.subject size="' + param + '" %}')
            self.assertNotIn("form-control-lg", res)
            self.assertNotIn("form-control-sm", res)
            self.assertNotIn("form-control-md", res)

        _test_size("sm", "form-control-sm")
        _test_size("lg", "form-control-lg")
        _test_size_medium("md")
        _test_size_medium("")

    def test_datetime(self):
        field = render_form_field("datetime")
        self.assertIn("vDateField", field)
        self.assertIn("vTimeField", field)

    def test_field_same_render(self):
        context = dict(form=TestForm())
        rendered_a = render_form_field("addon", context)
        rendered_b = render_form_field("addon", context)
        self.assertEqual(rendered_a, rendered_b)

    def test_label(self):
        res = render_template_with_form('{% bootstrap_label "foobar" label_for="subject" %}')
        self.assertEqual('<label for="subject">foobar</label>', res)

    def test_attributes_consistency(self):
        form = TestForm()
        attrs = form.fields["addon"].widget.attrs.copy()
        self.assertEqual(attrs, form.fields["addon"].widget.attrs)
