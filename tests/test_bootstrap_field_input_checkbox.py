from django import forms

from tests.base import BootstrapTestCase


class CheckboxTestForm(forms.Form):
    test = forms.BooleanField()


class InputTypeCheckboxTestCase(BootstrapTestCase):
    def test_input_type_checkbox(self):
        """Test field with checkbox widget."""
        self.assertHTMLEqual(
            self.render("{% bootstrap_field form.test %}", context={"form": CheckboxTestForm()}),
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
        """Test field with checkbox widget, style switch."""
        self.assertHTMLEqual(
            self.render(
                '{% bootstrap_field form.test checkbox_style="switch" %}', context={"form": CheckboxTestForm()}
            ),
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
        """Test field with checkbox widget, layout horizontal."""
        self.assertHTMLEqual(
            self.render("{% bootstrap_field form.test layout='horizontal' %}", context={"form": CheckboxTestForm()}),
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
