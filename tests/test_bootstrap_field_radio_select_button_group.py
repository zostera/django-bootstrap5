from django import forms

from django_bootstrap5.widgets import RadioSelectButtonGroup

from .base import BootstrapTestCase


class SelectTestForm(forms.Form):
    test = forms.ChoiceField(
        choices=(
            (1, "one"),
            (2, "two"),
        ),
        widget=RadioSelectButtonGroup,
    )


class DisabledSelectTestForm(forms.Form):
    test = forms.ChoiceField(
        choices=(
            (1, "one"),
            (2, "two"),
        ),
        widget=RadioSelectButtonGroup,
        disabled=True,
    )


class BootstrapFieldSelectTestCase(BootstrapTestCase):
    def test_select(self):
        """Test field with select widget."""
        self.assertHTMLEqual(
            self.render("{% bootstrap_field form.test %}", context={"form": SelectTestForm()}),
            (
                '<div class="django_bootstrap5-req mb-3">'
                '<label class="form-label">Test</label>'
                '<div id="id_test" class="btn-group" role="group">'
                '<input type="radio" class=" btn-check" autocomplete="off" name="test" id="id_test_0" value="1" '
                "required>"
                '<label class="btn btn-outline-primary" for="id_test_0">one</label>'
                '<input type="radio" class=" btn-check" autocomplete="off" name="test" id="id_test_1" value="2" '
                "required>"
                '<label class="btn btn-outline-primary" for="id_test_1">two</label>'
                "</div>"
                "</div>"
            ),
        )

    def test_select_horizontal(self):
        """Test field with select widget in horizontal layout."""
        self.assertHTMLEqual(
            self.render('{% bootstrap_field form.test layout="horizontal" %}', context={"form": SelectTestForm()}),
            (
                '<div class="django_bootstrap5-req row mb-3">'
                '<label class="col-sm-2 col-form-label">Test</label>'
                '<div class="col-sm-10">'
                '<div id="id_test" class="btn-group" role="group">'
                '<input type="radio" class=" btn-check" autocomplete="off" name="test" id="id_test_0" value="1" '
                "required>"
                '<label class="btn btn-outline-primary" for="id_test_0">one</label>'
                '<input type="radio" class=" btn-check" autocomplete="off" name="test" id="id_test_1" value="2" '
                "required>"
                '<label class="btn btn-outline-primary" for="id_test_1">two</label>'
                "</div>"
                "</div>"
                "</div>"
            ),
        )

    def test_select_floating(self):
        """Test field with select widget in floating layout."""
        self.assertHTMLEqual(
            self.render('{% bootstrap_field form.test layout="floating" %}', context={"form": SelectTestForm()}),
            (
                '<div class="django_bootstrap5-req mb-3">'
                '<label class="form-label">Test</label>'
                '<div id="id_test" class="btn-group" role="group">'
                '<input type="radio" class=" btn-check" autocomplete="off" name="test" id="id_test_0" value="1" '
                "required>"
                '<label class="btn btn-outline-primary" for="id_test_0">one</label>'
                '<input type="radio" class=" btn-check" autocomplete="off" name="test" id="id_test_1" value="2" '
                "required>"
                '<label class="btn btn-outline-primary" for="id_test_1">two</label>'
                "</div>"
                "</div>"
            ),
        )

    def test_disabled_select(self):
        """Test field with disabled select widget."""
        self.maxDiff = None
        self.assertHTMLEqual(
            self.render("{% bootstrap_field form.test %}", context={"form": DisabledSelectTestForm()}),
            (
                '<div class="django_bootstrap5-req mb-3">'
                '<label class="form-label">Test</label>'
                '<div id="id_test" class="btn-group" role="group">'
                '<input type="radio" class=" btn-check" autocomplete="off" name="test" id="id_test_0" value="1" '
                "disabled required>"
                '<label class="btn btn-outline-primary" for="id_test_0">one</label>'
                '<input type="radio" class=" btn-check" autocomplete="off" name="test" id="id_test_1" value="2" '
                "disabled required>"
                '<label class="btn btn-outline-primary" for="id_test_1">two</label>'
                "</div>"
                "</div>"
            ),
        )
