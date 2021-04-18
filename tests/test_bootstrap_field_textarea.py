from django import forms
from django.test import TestCase

from .base import render_template_with_bootstrap


class TestForm(forms.Form):
    test = forms.CharField(widget=forms.Textarea)


class BootstrapFieldTest(TestCase):
    def test_textarea(self):
        """Test field with textarea widget."""

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
