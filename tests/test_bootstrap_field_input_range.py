from django import forms

from tests.base import BootstrapTestCase


class RangeTestForm(forms.Form):
    test = forms.IntegerField(widget=forms.TextInput(attrs={"type": "range"}))


class InputTypeRangeTestCase(BootstrapTestCase):
    def test_input_type_range(self):
        """Test field with input widget with type `range`."""
        self.assertHTMLEqual(
            self.render("{% bootstrap_field form.test %}", context={"form": RangeTestForm()}),
            (
                '<div class="django_bootstrap5-req mb-3">'
                '<label for="id_test" class="form-label">Test</label>'
                '<input class="form-range" id="id_test" name="test" required type="range">'
                "</div>"
            ),
        )

    def test_input_type_range_horizontal(self):
        """Test field with input widget with type `range` in horizontal layout."""
        self.assertHTMLEqual(
            self.render('{% bootstrap_field form.test layout="horizontal" %}', context={"form": RangeTestForm()}),
            (
                '<div class="django_bootstrap5-req row mb-3">'
                '<label for="id_test" class="col-form-label col-sm-2">Test</label>'
                '<div class="col-sm-10">'
                '<input class="form-range" id="id_test" name="test" required type="range">'
                "</div>"
                "</div>"
            ),
        )

    def test_input_type_range_floating(self):
        """Test field with input widget with type `range` in floating layout."""
        self.assertHTMLEqual(
            self.render('{% bootstrap_field form.test layout="floating" %}', context={"form": RangeTestForm()}),
            (
                '<div class="django_bootstrap5-req mb-3">'
                '<label for="id_test" class="form-label">Test</label>'
                '<input class="form-range" id="id_test" name="test" required type="range">'
                "</div>"
            ),
        )

    def test_input_type_range_invalid(self):
        """Test that range input gets is-invalid class when bound with errors."""
        form = RangeTestForm(data={})
        html = self.render("{% bootstrap_field form.test %}", context={"form": form})
        self.assertIn("is-invalid", html)
        self.assertNotIn("is-valid", html)

    def test_input_type_range_valid(self):
        """Test that range input gets is-valid class when bound and valid."""
        form = RangeTestForm(data={"test": "5"})
        html = self.render("{% bootstrap_field form.test %}", context={"form": form})
        self.assertIn("is-valid", html)
        self.assertNotIn("is-invalid", html)
