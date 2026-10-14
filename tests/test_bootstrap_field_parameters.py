from django import forms

from tests.base import BootstrapTestCase


class CharFieldTestForm(forms.Form):
    test = forms.CharField()


class BootstrapFieldParameterTestCase(BootstrapTestCase):
    """Test `bootstrap_field` parameters`."""

    def test_wrapper_class(self):
        """Test field with default CharField widget."""
        form = CharFieldTestForm()

        self.assertHTMLEqual(
            self.render("{% bootstrap_field form.test %}", context={"form": form}),
            (
                '<div class="django_bootstrap5-req mb-3">'
                '<label for="id_test" class="form-label">Test</label>'
                '<input class="form-control" id="id_test" name="test" placeholder="Test" required type="text">'
                "</div>"
            ),
        )

        self.assertHTMLEqual(
            self.render("{% bootstrap_field form.test inline_wrapper_class='foo' %}", context={"form": form}),
            (
                '<div class="django_bootstrap5-req mb-3">'
                '<label for="id_test" class="form-label">Test</label>'
                '<input class="form-control" id="id_test" name="test" placeholder="Test" required type="text">'
                "</div>"
            ),
        )

        self.assertHTMLEqual(
            self.render("{% bootstrap_field form.test wrapper_class='foo' %}", context={"form": form}),
            (
                '<div class="django_bootstrap5-req foo">'
                '<label for="id_test" class="form-label">Test</label>'
                '<input class="form-control" id="id_test" name="test" placeholder="Test" required type="text">'
                "</div>"
            ),
        )

        self.assertHTMLEqual(
            self.render("{% bootstrap_field form.test wrapper_class=None %}", context={"form": form}),
            (
                '<div class="django_bootstrap5-req">'
                '<label for="id_test" class="form-label">Test</label>'
                '<input class="form-control" id="id_test" name="test" placeholder="Test" required type="text">'
                "</div>"
            ),
        )

    def test_inline_wrapper_class(self):
        """Test field with default CharField widget."""
        form = CharFieldTestForm()

        self.assertHTMLEqual(
            self.render("{% bootstrap_field form.test layout='inline' %}", context={"form": form}),
            (
                '<div class="col-12 django_bootstrap5-req">'
                '<label class="visually-hidden" for="id_test">Test</label>'
                '<input type="text" name="test" class="form-control" placeholder="Test" required id="id_test">'
                "</div>"
            ),
        )

        self.assertHTMLEqual(
            self.render("{% bootstrap_field form.test layout='inline' wrapper_class='foo' %}", context={"form": form}),
            (
                '<div class="col-12 django_bootstrap5-req">'
                '<label class="visually-hidden" for="id_test">Test</label>'
                '<input type="text" name="test" class="form-control" placeholder="Test" required id="id_test">'
                "</div>"
            ),
        )

        self.assertHTMLEqual(
            self.render(
                "{% bootstrap_field form.test layout='inline' inline_wrapper_class='foo' %}", context={"form": form}
            ),
            (
                '<div class="col-12 django_bootstrap5-req foo">'
                '<label class="visually-hidden" for="id_test">Test</label>'
                '<input type="text" name="test" class="form-control" placeholder="Test" required id="id_test">'
                "</div>"
            ),
        )


class InputGroupTestForm(forms.Form):
    first = forms.CharField(help_text="First help")
    second = forms.CharField(required=False)


class BootstrapFieldWrapperTestCase(BootstrapTestCase):
    """Test the `wrapper` parameter of `bootstrap_field`."""

    def test_wrapper_default_is_unchanged(self):
        """Test that not passing `wrapper` renders the wrapper as before."""
        self.assertHTMLEqual(
            self.render("{% bootstrap_field form.test %}", context={"form": CharFieldTestForm()}),
            (
                '<div class="django_bootstrap5-req mb-3">'
                '<label for="id_test" class="form-label">Test</label>'
                '<input class="form-control" id="id_test" name="test" placeholder="Test" required type="text">'
                "</div>"
            ),
        )

    def test_wrapper_false(self):
        """Test that `wrapper=False` renders label and field without a wrapper."""
        self.assertHTMLEqual(
            self.render("{% bootstrap_field form.test wrapper=False %}", context={"form": CharFieldTestForm()}),
            (
                '<label for="id_test" class="form-label">Test</label>'
                '<input class="form-control" id="id_test" name="test" placeholder="Test" required type="text">'
            ),
        )

    def test_wrapper_false_in_input_group(self):
        """Test that two fields without wrappers can share one input group."""
        self.assertHTMLEqual(
            self.render(
                '<div class="input-group">'
                "{% bootstrap_field form.first wrapper=False %}"
                "{% bootstrap_field form.second wrapper=False %}"
                "</div>",
                context={"form": InputGroupTestForm()},
            ),
            (
                '<div class="input-group">'
                '<label for="id_first" class="form-label">First</label>'
                '<input aria-describedby="id_first_helptext" class="form-control" id="id_first" name="first"'
                ' placeholder="First" required type="text">'
                '<div class="form-text" id="id_first_helptext">First help</div>'
                '<label for="id_second" class="form-label">Second</label>'
                '<input class="form-control" id="id_second" name="second" placeholder="Second" type="text">'
                "</div>"
            ),
        )

    def test_wrapper_false_keeps_errors_and_help_text(self):
        """Test that `wrapper=False` keeps the error block and the help text, and drops wrapper classes."""
        self.assertHTMLEqual(
            self.render(
                "{% bootstrap_field form.first wrapper=False %}", context={"form": InputGroupTestForm(data={})}
            ),
            (
                '<label for="id_first" class="form-label">First</label>'
                '<input aria-describedby="id_first_helptext id_first_error" aria-invalid="true"'
                ' class="form-control is-invalid" id="id_first" name="first" placeholder="First" required type="text">'
                '<div class="w-100" id="id_first_error">'
                '<div class="invalid-feedback d-block">This field is required.</div>'
                "</div>"
                '<div class="form-text" id="id_first_helptext">First help</div>'
            ),
        )

    def test_wrapper_false_keeps_form_floating(self):
        """Test that `wrapper=False` keeps a `form-floating` element for a floating label."""
        self.assertHTMLEqual(
            self.render(
                "{% bootstrap_field form.test layout='floating' wrapper=False %}",
                context={"form": CharFieldTestForm()},
            ),
            (
                '<div class="form-floating">'
                '<input class="form-control" id="id_test" name="test" placeholder="Test" required type="text">'
                '<label for="id_test" class="form-label">Test</label>'
                "</div>"
            ),
        )

    def test_wrapper_false_on_form(self):
        """Test that `wrapper=False` on `bootstrap_form` reaches the fields."""
        self.assertHTMLEqual(
            self.render("{% bootstrap_form form wrapper=False %}", context={"form": CharFieldTestForm()}),
            (
                '<label for="id_test" class="form-label">Test</label>'
                '<input class="form-control" id="id_test" name="test" placeholder="Test" required type="text">'
            ),
        )
