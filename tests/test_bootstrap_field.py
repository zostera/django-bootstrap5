from django import forms
from django.test import TestCase

from .test_templates import render_template_with_bootstrap


class BootstrapFieldTest(TestCase):
    def test_bootstrap_field_text(self):
        class TestForm(forms.Form):
            name = forms.CharField()

        test_form = TestForm()
        html = render_template_with_bootstrap("{% bootstrap_field form.name %}", context={"form": test_form})
        self.assertHTMLEqual(
            html,
            (
                '<div class="mb-3">'
                '<label for="id_name" class="form-label">Name</label>'
                '<input class="form-control" id="id_name" name="name" placeholder="Name" required type="text">'
                "</div>"
            ),
        )
