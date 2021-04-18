from django import forms
from django.test import TestCase

from .base import render_template_with_bootstrap


class BootstrapFieldTest(TestCase):
    def test_bootstrap_field_text_floating(self):
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
