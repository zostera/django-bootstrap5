from django import forms
from django.test import TestCase

from .base import render_template_with_bootstrap


class BootstrapHorizontalFieldTest(TestCase):
    def test_bootstrap_field_text_horizontal(self):
        """Test field with text widget."""

        class TestForm(forms.Form):
            test = forms.CharField()

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
