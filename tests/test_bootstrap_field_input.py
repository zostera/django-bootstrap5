from django import forms
from django.core.files.uploadedfile import SimpleUploadedFile
from django.forms import TextInput
from django.test import TestCase

from .base import render_template_with_bootstrap


class TestForm(forms.Form):
    test = forms.CharField()


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

    def test_bootstrap_field_text_horizontal(self):
        """Test field with text widget."""

        test_form = TestForm()
        html = render_template_with_bootstrap(
            "{% bootstrap_field form.test layout='horizontal' %}", context={"form": test_form}
        )
        self.assertHTMLEqual(
            html,
            (
                '<div class="django_bootstrap5-req mb-3 row">'
                '<label class="col-form-label col-sm-2" for="id_test">'
                "Test"
                '</label><div class="col-sm-10">'
                '<input class="form-control" id="id_test" name="test" placeholder="Test" required type="text">'
                "</div>"
                "</div>"
            ),
        )

    def test_input_type_text_floating(self):
        """Test field with text widget in floating layout."""

        class TestForm(forms.Form):
            test = forms.CharField()

        test_form = TestForm()
        html = render_template_with_bootstrap(
            "{% bootstrap_field form.test layout='floating' %}", context={"form": test_form}
        )
        self.assertHTMLEqual(
            html,
            (
                '<div class="django_bootstrap5-req mb-3 form-floating">'
                '<input class="form-control" id="id_test" name="test" placeholder="Test" required type="text">'
                '<label for="id_test" class="form-label">Test</label>'
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

    def test_bootstrap_field_checkbox_horizontal(self):
        """Test field with text widget."""

        class TestForm(forms.Form):
            test = forms.BooleanField()

        test_form = TestForm()
        html = render_template_with_bootstrap(
            "{% bootstrap_field form.test layout='horizontal' %}", context={"form": test_form}
        )
        self.assertHTMLEqual(
            html,
            (
                '<div class="django_bootstrap5-req mb-3 row">'
                '<div class="col-sm-10 offset-sm-2">'
                '<div class="form-check">'
                '<input class="form-check-input" id="id_test" name="test" required type="checkbox">'
                '<label class="form-check-label" for="id_test">'
                "Test"
                "</label>"
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
