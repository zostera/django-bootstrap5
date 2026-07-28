from django import forms

from .base import BootstrapTestCase


class CheckboxSelectMultipleWithAttrs(forms.CheckboxSelectMultiple):
    """Widget that adds a custom attribute to each option (#300)."""

    def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
        option = super().create_option(name, value, label, selected, index, subindex, attrs)
        option["attrs"]["data-total"] = "5220"
        return option


class CheckboxSelectMultipleTestForm(forms.Form):
    test = forms.MultipleChoiceField(
        choices=(
            (1, "one"),
            (2, "two"),
        ),
        widget=CheckboxSelectMultipleWithAttrs,
        required=False,
    )


class BootstrapFieldCheckboxSelectMultipleTestCase(BootstrapTestCase):
    def test_custom_option_attrs_preserved(self):
        """Custom attrs added in create_option() must survive rendering (#300)."""
        html = self.render("{% bootstrap_field form.test %}", context={"form": CheckboxSelectMultipleTestForm()})
        self.assertIn('data-total="5220"', html)
        self.assertHTMLEqual(
            html,
            (
                '<div class="mb-3">'
                '<label class="form-label">Test</label>'
                '<div id="id_test">'
                '<div class="form-check">'
                '<input class="form-check-input" type="checkbox" name="test" id="id_test_0" value="1"'
                ' data-total="5220">'
                '<label class="form-check-label" for="id_test_0">one</label>'
                "</div>"
                '<div class="form-check">'
                '<input class="form-check-input" type="checkbox" name="test" id="id_test_1" value="2"'
                ' data-total="5220">'
                '<label class="form-check-label" for="id_test_1">two</label>'
                "</div>"
                "</div>"
                "</div>"
            ),
        )
