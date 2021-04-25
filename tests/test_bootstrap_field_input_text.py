from django import forms
from django.forms import TextInput

from tests.base import BootstrapTestCase


class InputTypeTextTestCase(BootstrapTestCase):
    """Test for TextInput widgets that only differ in type, and have no other exceptions."""

    def _html_default(self, input_type):
        """Output for input with given input_type in default layout."""
        return (
            '<div class="django_bootstrap5-req mb-3">'
            '<label for="id_test" class="form-label">Test</label>'
            f'<input class="form-control" id="id_test" name="test" placeholder="Test" required type="{input_type}">'
            "</div>"
        )

    def _html_horizontal(self, input_type):
        """Output for input with given input_type in horizontal layout."""
        return (
            '<div class="django_bootstrap5-req mb-3 row">'
            '<label class="col-form-label col-sm-2" for="id_test">'
            "Test"
            '</label><div class="col-sm-10">'
            f'<input class="form-control" id="id_test" name="test" placeholder="Test" required type="{input_type}">'
            "</div>"
            "</div>"
        )

    def _html_floating(self, input_type):
        """
        Output for input with given input_type in floating layout.

        Note that this function does not check if the flaoting layout is supported for this input_type.
        """
        return (
            '<div class="django_bootstrap5-req mb-3 form-floating">'
            f'<input class="form-control" id="id_test" name="test" placeholder="Test" required type="{input_type}">'
            '<label for="id_test" class="form-label">Test</label>'
            "</div>"
        )

    def test_input_type_text(self):
        """Test field with default CharField widget."""

        class TextTestForm(forms.Form):
            test = forms.CharField()

        form = TextTestForm()

        self.assertHTMLEqual(
            self.render("{% bootstrap_field form.test %}", context={"form": form}),
            self._html_default("text"),
        )

        self.assertHTMLEqual(
            self.render("{% bootstrap_field form.test layout='horizontal' %}", context={"form": form}),
            self._html_horizontal("text"),
        ),

        self.assertHTMLEqual(
            self.render("{% bootstrap_field form.test layout='floating' %}", context={"form": form}),
            self._html_floating("text"),
        )

    def _test_input_type(self, input_type):
        """Test field with given input type in all layouts."""

        class InputTypeTestForm(forms.Form):
            test = forms.CharField(widget=TextInput(attrs={"type": input_type}))

        form = InputTypeTestForm()
        default_html = self._html_default(input_type)
        horizontal_html = self._html_horizontal(input_type)
        floating_html = self._html_floating(input_type)

        self.assertHTMLEqual(
            self.render("{% bootstrap_field form.test %}", context={"form": form}),
            default_html,
        )

        self.assertHTMLEqual(
            self.render("{% bootstrap_field form.test layout='horizontal' %}", context={"form": form}),
            horizontal_html,
        )

        self.assertHTMLEqual(
            self.render("{% bootstrap_field form.test layout='floating' %}", context={"form": form}),
            floating_html,
        )

    def test_input_types(self):
        """Test field with CharField widget and its type set."""
        self._test_input_type("text")
        self._test_input_type("number")
        self._test_input_type("email")
        self._test_input_type("url")
        self._test_input_type("tel")
        self._test_input_type("date")
        self._test_input_type("time")
        self._test_input_type("password")

    def test_input_type_password(self):
        """Test field with password widget."""

        class PasswordTestForm(forms.Form):
            test = forms.CharField(widget=forms.PasswordInput)

        form = PasswordTestForm()

        self.assertHTMLEqual(
            self.render("{% bootstrap_field form.test %}", context={"form": form}),
            self._html_default("password"),
        )

        self.assertHTMLEqual(
            self.render("{% bootstrap_field form.test layout='horizontal' %}", context={"form": form}),
            self._html_horizontal("password"),
        ),

        self.assertHTMLEqual(
            self.render("{% bootstrap_field form.test layout='floating' %}", context={"form": form}),
            self._html_floating("password"),
        )
