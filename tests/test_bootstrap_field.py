from django import forms
from django.test import TestCase

from .test_templates import render_template_with_bootstrap


class BootstrapFieldTest(TestCase):
    def test_bootstrap_field_text(self):
        class TestForm(forms.Form):
            name = forms.CharField()

        test_form = TestForm()
        test_form.fields["name"].widget.attrs["class"] = "form-control"
        html = render_template_with_bootstrap("{{ form.name }}", context={"form": test_form})
        self.assertHTMLEqual(html, '<input type="text" class="form-control" id="id_name" name="name" required>')
