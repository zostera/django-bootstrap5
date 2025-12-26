from django import forms
from django.contrib.admin.widgets import AdminSplitDateTime

from tests.base import DJANGO_VERSION, BootstrapTestCase


class DateTimeTestForm(forms.Form):
    test = forms.SplitDateTimeField(widget=AdminSplitDateTime())


class DateTimeTestCase(BootstrapTestCase):
    def test_input_type_admin_split_date_time(self):
        """Test field with AdminSplitDateTime widget."""
        if DJANGO_VERSION >= "6.0":
            expected_html = (
                '<div class="mb-3 django_bootstrap5-req">'
                '<label class="form-label" for="id_test">Test</label>'
                '<p class="datetime">'
                '<label for="id_test_0">Date:</label> '
                ' <input type="text" name="test_0" class="form-control vDateField" size="10"'
                ' placeholder="Test" required id="id_test_0" aria-describedby="id_test_timezone_warning_helptext">'
                "<br>"
                '<label for="id_test_1">Time:</label>'
                ' <input type="text" name="test_1" class="form-control vTimeField" size="8"'
                ' placeholder="Test" required id="id_test_1" aria-describedby="id_test_timezone_warning_helptext">'
                "</p>"
                "</div>"
            )
        else:
            expected_html = (
                '<div class="django_bootstrap5-req mb-3">'
                '<label class="form-label">Test</label>'
                '<p class="datetime">'
                "Date: "
                '<input type="text" name="test_0" class="form-control vDateField" size="10"'
                ' placeholder="Test" required id="id_test_0">'
                "<br>"
                "Time: "
                '<input type="text" name="test_1" class="form-control vTimeField" size="8"'
                ' placeholder="Test" required id="id_test_1">'
                "</p>"
                "</div>"
            )
        html = self.render("{% bootstrap_field form.test %}", context={"form": DateTimeTestForm()})
        self.assertHTMLEqual(
            html,
            expected_html,
        )

    def test_input_type_admin_split_date_time_horizontal(self):
        """Test field with AdminSplitDateTime widget with layout horizontal."""
        if DJANGO_VERSION >= "6.0":
            expected_html = (
                '<div class="row mb-3 django_bootstrap5-req">'
                '<label class="col-sm-2 col-form-label" for="id_test">Test</label>'
                '<div class="col-sm-10"><p class="datetime">'
                '<label for="id_test_0">Date:</label>'
                ' <input type="text" name="test_0" class="form-control vDateField" size="10"'
                ' placeholder="Test" required id="id_test_0" aria-describedby="id_test_timezone_warning_helptext">'
                "<br>"
                '<label for="id_test_1">Time:</label>'
                ' <input type="text" name="test_1" class="form-control vTimeField" size="8"'
                ' placeholder="Test" required id="id_test_1" aria-describedby="id_test_timezone_warning_helptext">'
                "</p>"
                "</div>"
                "</div>"
            )
        else:
            expected_html = (
                '<div class="django_bootstrap5-req row mb-3">'
                '<label class="col-form-label col-sm-2">Test</label>'
                '<div class="col-sm-10">'
                '<p class="datetime">'
                "Date: "
                '<input type="text" name="test_0" class="form-control vDateField" size="10"'
                ' placeholder="Test" required id="id_test_0">'
                "<br>"
                "Time: "
                '<input type="text" name="test_1" class="form-control vTimeField" size="8"'
                ' placeholder="Test" required id="id_test_1">'
                "</p>"
                "</div>"
                "</div>"
            )
        html = self.render(
            '{% bootstrap_field form.test layout="horizontal" %}',
            context={"form": DateTimeTestForm()},
        )
        self.assertHTMLEqual(
            html,
            expected_html,
        )

    def test_input_type_admin_split_date_time_floating(self):
        """Test field with AdminSplitDateTime widget with layout floating."""
        if DJANGO_VERSION >= "6.0":
            expected_html = (
                '<div class="mb-3 django_bootstrap5-req">'
                '<label class="form-label" for="id_test">Test</label>'
                '<p class="datetime">'
                '<label for="id_test_0">Date:</label>'
                ' <input type="text" name="test_0" class="form-control vDateField" size="10"'
                ' placeholder="Test" required id="id_test_0" aria-describedby="id_test_timezone_warning_helptext">'
                "<br>"
                '<label for="id_test_1">Time:</label>'
                ' <input type="text" name="test_1" class="form-control vTimeField" size="8"'
                ' placeholder="Test" required id="id_test_1" aria-describedby="id_test_timezone_warning_helptext">'
                "</p>"
                "</div>"
            )
        else:
            expected_html = (
                '<div class="django_bootstrap5-req mb-3">'
                '<div class="form-floating">'
                '<input type="text" name="test_0" class="form-control vDateField" size="10"'
                ' placeholder="Test" required id="id_test_0">'
                '<label for="id_test_0">Test - Date:</label>'
                "</div>"
                '<div class="form-floating mt-2">'
                '<input type="text" name="test_1" class="form-control vTimeField" size="8"'
                ' placeholder="Test" required id="id_test_1">'
                '<label for="id_test_1">Test - Time:</label>'
                "</div>"
                "</div>"
            )
        html = self.render(
            '{% bootstrap_field form.test layout="floating" %}',
            context={"form": DateTimeTestForm()},
        )
        self.assertHTMLEqual(
            html,
            expected_html,
        )
