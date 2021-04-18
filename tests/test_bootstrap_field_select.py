from django import forms
from django.test import TestCase

from .base import render_template_with_bootstrap


class TestForm(forms.Form):
    test = forms.ChoiceField(
        choices=(
            (1, "one"),
            (2, "two"),
        )
    )


class BootstrapFieldSelectTest(TestCase):
    def test_select(self):
        """Test field with text widget."""

        test_form = TestForm()
        html = render_template_with_bootstrap("{% bootstrap_field form.test %}", context={"form": test_form})
        self.assertHTMLEqual(
            html,
            (
                '<div class="django_bootstrap5-req mb-3">'
                '<label for="id_test" class="form-label">Test</label>'
                '<select class="form-select" id="id_test" name="test">'
                '<option value="1">one</option>'
                '<option value="2">two</option>'
                "</select>"
                "</div>"
            ),
        )

    def test_select_floating(self):
        """Test field with text widget."""

        test_form = TestForm()
        html = render_template_with_bootstrap(
            '{% bootstrap_field form.test layout="floating" %}', context={"form": test_form}
        )
        self.assertHTMLEqual(
            html,
            (
                '<div class="django_bootstrap5-req form-floating mb-3">'
                '<select class="form-select" id="id_test" name="test">'
                '<option value="1">one</option>'
                '<option value="2">two</option>'
                "</select>"
                '<label for="id_test" class="form-label">Test</label>'
                "</div>"
            ),
        )
