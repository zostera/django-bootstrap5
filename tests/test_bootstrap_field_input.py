from django import forms
from django.core.files.uploadedfile import SimpleUploadedFile
from django.forms import TextInput
from django.test import TestCase

from .base import render_template_with_bootstrap


class TextTestForm(forms.Form):
    test = forms.CharField()


class FileFieldTestForm(forms.Form):
    test = forms.FileField()


class ClearableFileInputTestForm(forms.Form):
    test = forms.FileField(widget=forms.ClearableFileInput, required=False)


class CheckboxTestForm(forms.Form):
    test = forms.BooleanField()


class ColorTestForm(forms.Form):
    test = forms.CharField(widget=TextInput(attrs={"type": "color"}))


class RangeTestForm(forms.Form):
    test = forms.IntegerField(widget=TextInput(attrs={"type": "range"}))


class InputTypeTextTestCase(TestCase):
    def test_input_type_text(self):
        """Test field with text widget."""

        test_form = TextTestForm()
        self.assertHTMLEqual(
            render_template_with_bootstrap("{% bootstrap_field form.test %}", context={"form": test_form}),
            (
                '<div class="django_bootstrap5-req mb-3">'
                '<label for="id_test" class="form-label">Test</label>'
                '<input class="form-control" id="id_test" name="test" placeholder="Test" required type="text">'
                "</div>"
            ),
        )

    def test_bootstrap_field_text_horizontal(self):
        """Test field with text widget."""

        test_form = TextTestForm()
        self.assertHTMLEqual(
            render_template_with_bootstrap(
                "{% bootstrap_field form.test layout='horizontal' %}", context={"form": test_form}
            ),
            (
                '<div class="django_bootstrap5-req mb-3 row">'
                '<label class="col-form-label col-sm-2" for="id_test">'
                "Test"
                '</label><div class="col-sm-10">'
                '<input class="form-control" id="id_test" name="test" placeholder="Test" required type="text">'
                "</div>"
                "</div>"
            ),
        )

    def test_input_type_text_floating(self):
        """Test field with text widget in floating layout."""

        test_form = TextTestForm()
        self.assertHTMLEqual(
            render_template_with_bootstrap(
                "{% bootstrap_field form.test layout='floating' %}", context={"form": test_form}
            ),
            (
                '<div class="django_bootstrap5-req mb-3 form-floating">'
                '<input class="form-control" id="id_test" name="test" placeholder="Test" required type="text">'
                '<label for="id_test" class="form-label">Test</label>'
                "</div>"
            ),
        )


class InputTypeColorTestCase(TestCase):
    def test_input_type_color(self):
        """Test field with input widget with type `color`."""

        test_form = ColorTestForm()
        self.assertHTMLEqual(
            render_template_with_bootstrap("{% bootstrap_field form.test %}", context={"form": test_form}),
            (
                '<div class="django_bootstrap5-req mb-3">'
                '<label for="id_test" class="form-label">Test</label>'
                '<input class="form-control form-control-color" '
                'id="id_test" name="test" placeholder="Test" required type="color">'
                "</div>"
            ),
        )

    def test_input_type_color_horizontal(self):
        """Test field with input widget with type `color` in horizontal layout."""

        test_form = ColorTestForm()
        self.assertHTMLEqual(
            render_template_with_bootstrap(
                '{% bootstrap_field form.test layout="horizontal" %}', context={"form": test_form}
            ),
            (
                '<div class="django_bootstrap5-req row mb-3">'
                '<label for="id_test" class="col-form-label col-sm-2">Test</label>'
                '<div class="col-sm-10">'
                '<input class="form-control form-control-color" id="id_test"'
                ' name="test" placeholder="Test" required type="color">'
                "</div>"
                "</div>"
            ),
        )

    def test_input_type_color_floating(self):
        """Test field with input widget with type `color` in floating layout."""

        test_form = ColorTestForm()
        self.assertHTMLEqual(
            render_template_with_bootstrap(
                '{% bootstrap_field form.test layout="floating" %}', context={"form": test_form}
            ),
            (
                '<div class="django_bootstrap5-req mb-3">'
                '<label for="id_test" class="form-label">Test</label>'
                '<input class="form-control form-control-color" id="id_test"'
                ' name="test" placeholder="Test" required type="color">'
                "</div>"
            ),
        )


class InputTypeRangeTestCase(TestCase):
    def test_input_type_range(self):
        """Test field with input widget with type `range`."""

        test_form = RangeTestForm()

        self.assertHTMLEqual(
            render_template_with_bootstrap("{% bootstrap_field form.test %}", context={"form": test_form}),
            (
                '<div class="django_bootstrap5-req mb-3">'
                '<label for="id_test" class="form-label">Test</label>'
                '<input class="form-range" id="id_test" name="test" placeholder="Test" required type="range">'
                "</div>"
            ),
        )

    def test_input_type_range_horizontal(self):
        """Test field with input widget with type `range` in horizontal layout."""

        test_form = RangeTestForm()
        self.assertHTMLEqual(
            render_template_with_bootstrap(
                '{% bootstrap_field form.test layout="horizontal" %}', context={"form": test_form}
            ),
            (
                '<div class="django_bootstrap5-req row mb-3">'
                '<label for="id_test" class="col-form-label col-sm-2">Test</label>'
                '<div class="col-sm-10">'
                '<input class="form-range" id="id_test" name="test" placeholder="Test" required type="range">'
                "</div>"
                "</div>"
            ),
        )

    def test_input_type_range_floating(self):
        """Test field with input widget with type `range` in floating layout."""

        test_form = RangeTestForm()
        self.assertHTMLEqual(
            render_template_with_bootstrap(
                '{% bootstrap_field form.test layout="floating" %}', context={"form": test_form}
            ),
            (
                '<div class="django_bootstrap5-req mb-3">'
                '<label for="id_test" class="form-label">Test</label>'
                '<input class="form-range" id="id_test" name="test" placeholder="Test" required type="range">'
                "</div>"
            ),
        )


class InputTypeCheckboxTestCase(TestCase):
    def test_input_type_checkbox(self):
        """Test field with checkbox widget."""

        test_form = CheckboxTestForm()
        self.assertHTMLEqual(
            render_template_with_bootstrap("{% bootstrap_field form.test %}", context={"form": test_form}),
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

        test_form = CheckboxTestForm()
        self.assertHTMLEqual(
            render_template_with_bootstrap(
                '{% bootstrap_field form.test checkbox_style="switch" %}', context={"form": test_form}
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

        test_form = CheckboxTestForm()
        self.assertHTMLEqual(
            render_template_with_bootstrap(
                "{% bootstrap_field form.test layout='horizontal' %}", context={"form": test_form}
            ),
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


class InputTypeFileTestCase(TestCase):
    def test_input_type_file(self):

        test_form = FileFieldTestForm()
        self.assertHTMLEqual(
            render_template_with_bootstrap("{% bootstrap_field form.test %}", context={"form": test_form}),
            (
                '<div class="django_bootstrap5-req mb-3">'
                '<label for="id_test" class="form-label">Test</label>'
                '<input class="form-control" id="id_test" name="test" required type="file">'
                "</div>"
            ),
        )

    def test_clearable_file_input(self):

        test_form = ClearableFileInputTestForm()
        self.assertHTMLEqual(
            render_template_with_bootstrap("{% bootstrap_field form.test %}", context={"form": test_form}),
            (
                '<div class="mb-3">'
                '<label for="id_test" class="form-label">Test</label>'
                '<input class="form-control" id="id_test" name="test" type="file">'
                "</div>"
            ),
        )

    def test_clearable_file_input_post(self):

        test_form = ClearableFileInputTestForm({}, {"test": SimpleUploadedFile("test.txt", b"test")})
        self.assertHTMLEqual(
            render_template_with_bootstrap("{% bootstrap_field form.test %}", context={"form": test_form}),
            (
                '<div class="django_bootstrap5-bound mb-3">'
                '<label class="form-label" for="id_test">Test</label>'
                '<input type="file" name="test" class="form-control django_bootstrap5-bound" id="id_test">'
                "</div>"
            ),
        )
