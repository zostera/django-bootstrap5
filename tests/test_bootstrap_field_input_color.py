from django import forms

from tests.base import BootstrapTestCase


class ColorTestForm(forms.Form):
    test = forms.CharField(widget=forms.TextInput(attrs={"type": "color"}))


class InputTypeColorTestCase(BootstrapTestCase):
    def test_input_type_color(self):
        """Test field with input widget with type `color`."""
        self.assertHTMLEqual(
            self.render("{% bootstrap_field form.test %}", context={"form": ColorTestForm()}),
            (
                '<div class="django_bootstrap5-req mb-3">'
                '<label for="id_test" class="form-label">Test</label>'
                '<input class="form-control form-control-color" '
                'id="id_test" name="test" required type="color">'
                "</div>"
            ),
        )

    def test_input_type_color_horizontal(self):
        """Test field with input widget with type `color` in horizontal layout."""
        self.assertHTMLEqual(
            self.render('{% bootstrap_field form.test layout="horizontal" %}', context={"form": ColorTestForm()}),
            (
                '<div class="django_bootstrap5-req row mb-3">'
                '<label for="id_test" class="col-form-label col-sm-2">Test</label>'
                '<div class="col-sm-10">'
                '<input class="form-control form-control-color" id="id_test"'
                ' name="test" required type="color">'
                "</div>"
                "</div>"
            ),
        )

    def test_input_type_color_addon(self):
        """Test field with input widget with type `color` and an addon (#872)."""
        self.assertHTMLEqual(
            self.render('{% bootstrap_field form.test addon_before="$" %}', context={"form": ColorTestForm()}),
            (
                '<div class="django_bootstrap5-req mb-3">'
                '<label for="id_test" class="form-label">Test</label>'
                '<div class="input-group">'
                '<span class="input-group-text">$</span>'
                '<input class="form-control form-control-color" id="id_test"'
                ' name="test" required type="color">'
                "</div>"
                "</div>"
            ),
        )

    def test_input_type_color_floating(self):
        """Test field with input widget with type `color` in floating layout."""
        self.assertHTMLEqual(
            self.render('{% bootstrap_field form.test layout="floating" %}', context={"form": ColorTestForm()}),
            (
                '<div class="django_bootstrap5-req mb-3">'
                '<label for="id_test" class="form-label">Test</label>'
                '<input class="form-control form-control-color" id="id_test"'
                ' name="test" required type="color">'
                "</div>"
            ),
        )

    def test_input_type_color_addon_floating(self):
        """A color input takes an addon but still does not float, so it gets a plain input group."""
        self.assertHTMLEqual(
            self.render(
                '{% bootstrap_field form.test addon_before="$" layout="floating" %}',
                context={"form": ColorTestForm()},
            ),
            (
                '<div class="django_bootstrap5-req mb-3">'
                '<label for="id_test" class="form-label">Test</label>'
                '<div class="input-group">'
                '<span class="input-group-text">$</span>'
                '<input class="form-control form-control-color" id="id_test"'
                ' name="test" required type="color">'
                "</div>"
                "</div>"
            ),
        )
