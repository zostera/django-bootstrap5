from django import forms
from django.core.files.uploadedfile import SimpleUploadedFile
from django.forms import TextInput

from tests.base import BootstrapTestCase


class TextTestForm(forms.Form):
    test = forms.CharField()


class PasswordTestForm(forms.Form):
    test = forms.CharField(widget=forms.PasswordInput)


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


class InputTypeTextTestCase(BootstrapTestCase):
    def test_input_type_text(self):
        """Test field with text widget."""
        self.assertHTMLEqual(
            self.render("{% bootstrap_field form.test %}", context={"form": TextTestForm()}),
            (
                '<div class="django_bootstrap5-req mb-3">'
                '<label for="id_test" class="form-label">Test</label>'
                '<input class="form-control" id="id_test" name="test" placeholder="Test" required type="text">'
                "</div>"
            ),
        )

    def test_bootstrap_field_text_horizontal(self):
        """Test field with text widget."""
        self.assertHTMLEqual(
            self.render("{% bootstrap_field form.test layout='horizontal' %}", context={"form": TextTestForm()}),
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
        self.assertHTMLEqual(
            self.render("{% bootstrap_field form.test layout='floating' %}", context={"form": TextTestForm()}),
            (
                '<div class="django_bootstrap5-req mb-3 form-floating">'
                '<input class="form-control" id="id_test" name="test" placeholder="Test" required type="text">'
                '<label for="id_test" class="form-label">Test</label>'
                "</div>"
            ),
        )

    def test_input_type_password(self):
        """Test field with password widget."""
        self.assertHTMLEqual(
            self.render("{% bootstrap_field form.test %}", context={"form": PasswordTestForm()}),
            (
                '<div class="django_bootstrap5-req mb-3">'
                '<label for="id_test" class="form-label">Test</label>'
                '<input class="form-control" id="id_test" name="test" placeholder="Test" required type="password">'
                "</div>"
            ),
        )

    def test_bootstrap_field_password_horizontal(self):
        """Test field with password widget."""
        self.assertHTMLEqual(
            self.render("{% bootstrap_field form.test layout='horizontal' %}", context={"form": PasswordTestForm()}),
            (
                '<div class="django_bootstrap5-req mb-3 row">'
                '<label class="col-form-label col-sm-2" for="id_test">'
                "Test"
                '</label><div class="col-sm-10">'
                '<input class="form-control" id="id_test" name="test" placeholder="Test" required type="password">'
                "</div>"
                "</div>"
            ),
        )

    def test_input_type_password_floating(self):
        """Test field with password widget in floating layout."""
        self.assertHTMLEqual(
            self.render("{% bootstrap_field form.test layout='floating' %}", context={"form": PasswordTestForm()}),
            (
                '<div class="django_bootstrap5-req mb-3 form-floating">'
                '<input class="form-control" id="id_test" name="test" placeholder="Test" required type="password">'
                '<label for="id_test" class="form-label">Test</label>'
                "</div>"
            ),
        )


class InputTypeColorTestCase(BootstrapTestCase):
    def test_input_type_color(self):
        """Test field with input widget with type `color`."""
        self.assertHTMLEqual(
            self.render("{% bootstrap_field form.test %}", context={"form": ColorTestForm()}),
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
        self.assertHTMLEqual(
            self.render('{% bootstrap_field form.test layout="horizontal" %}', context={"form": ColorTestForm()}),
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
        self.assertHTMLEqual(
            self.render('{% bootstrap_field form.test layout="floating" %}', context={"form": ColorTestForm()}),
            (
                '<div class="django_bootstrap5-req mb-3">'
                '<label for="id_test" class="form-label">Test</label>'
                '<input class="form-control form-control-color" id="id_test"'
                ' name="test" placeholder="Test" required type="color">'
                "</div>"
            ),
        )


class InputTypeRangeTestCase(BootstrapTestCase):
    def test_input_type_range(self):
        """Test field with input widget with type `range`."""
        self.assertHTMLEqual(
            self.render("{% bootstrap_field form.test %}", context={"form": RangeTestForm()}),
            (
                '<div class="django_bootstrap5-req mb-3">'
                '<label for="id_test" class="form-label">Test</label>'
                '<input class="form-range" id="id_test" name="test" placeholder="Test" required type="range">'
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
                '<input class="form-range" id="id_test" name="test" placeholder="Test" required type="range">'
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
                '<input class="form-range" id="id_test" name="test" placeholder="Test" required type="range">'
                "</div>"
            ),
        )


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


class InputTypeFileTestCase(BootstrapTestCase):
    def test_input_type_file(self):
        self.assertHTMLEqual(
            self.render("{% bootstrap_field form.test %}", context={"form": FileFieldTestForm()}),
            (
                '<div class="django_bootstrap5-req mb-3">'
                '<label for="id_test" class="form-label">Test</label>'
                '<input class="form-control" id="id_test" name="test" required type="file">'
                "</div>"
            ),
        )

    def test_clearable_file_input(self):
        self.assertHTMLEqual(
            self.render("{% bootstrap_field form.test %}", context={"form": ClearableFileInputTestForm()}),
            (
                '<div class="mb-3">'
                '<label for="id_test" class="form-label">Test</label>'
                '<input class="form-control" id="id_test" name="test" type="file">'
                "</div>"
            ),
        )

    def test_clearable_file_input_post(self):
        self.assertHTMLEqual(
            self.render(
                "{% bootstrap_field form.test %}",
                context={"form": ClearableFileInputTestForm({}, {"test": SimpleUploadedFile("test.txt", b"test")})},
            ),
            (
                '<div class="django_bootstrap5-bound mb-3">'
                '<label class="form-label" for="id_test">Test</label>'
                '<input type="file" name="test" class="form-control django_bootstrap5-bound" id="id_test">'
                "</div>"
            ),
        )
