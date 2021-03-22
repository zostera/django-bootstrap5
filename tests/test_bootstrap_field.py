from django import forms
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from django_bootstrap5.exceptions import BootstrapError

from .base import (
    TestForm,
    html_39x27,
    render_field,
    render_form_field,
    render_template_with_bootstrap,
    render_template_with_form,
)


class BootstrapFieldTest(TestCase):
    def test_bootstrap_field_text(self):
        """Test field with text widget."""

        class TestForm(forms.Form):
            test = forms.CharField()

        test_form = TestForm()
        html = render_template_with_bootstrap("{% bootstrap_field form.test %}", context={"form": test_form})
        self.assertHTMLEqual(
            html,
            (
                '<div class="django_bootstrap5-req mb-3">'
                '<label for="id_test" class="form-label">Test</label>'
                '<input class="form-control" id="id_test" name="test" placeholder="Test" required type="text">'
                "</div>"
            ),
        )

    def test_bootstrap_field_text_floating(self):
        """Test field with text widget in floating layout."""

        class TestForm(forms.Form):
            test = forms.CharField()

        test_form = TestForm()
        html = render_template_with_bootstrap(
            "{% bootstrap_field form.test layout='floating' %}", context={"form": test_form}
        )
        self.assertHTMLEqual(
            html,
            (
                '<div class="django_bootstrap5-req mb-3 form-floating">'
                '<input class="form-control" id="id_test" name="test" placeholder="Test" required type="text">'
                '<label for="id_test" class="form-label">Test</label>'
                "</div>"
            ),
        )

    def test_bootstrap_field_file(self):
        class TestForm(forms.Form):
            test = forms.FileField()

        test_form = TestForm()
        html = render_template_with_bootstrap("{% bootstrap_field form.test %}", context={"form": test_form})
        self.assertHTMLEqual(
            html,
            (
                '<div class="django_bootstrap5-req mb-3">'
                '<label for="id_test" class="form-label">Test</label>'
                '<input class="form-control" id="id_test" name="test" required type="file">'
                "</div>"
            ),
        )

    def test_bootstrap_field_clearable_file(self):
        class TestForm(forms.Form):
            test = forms.FileField(widget=forms.ClearableFileInput, required=False)

        test_form = TestForm()
        self.assertHTMLEqual(
            render_template_with_bootstrap("{% bootstrap_field form.test %}", context={"form": test_form}),
            (
                '<div class="mb-3">'
                '<label for="id_test" class="form-label">Test</label>'
                '<input class="form-control" id="id_test" name="test" type="file">'
                "</div>"
            ),
        )

    def test_bootstrap_field_clearable_file_post(self):
        class TestForm(forms.Form):
            test = forms.FileField(widget=forms.ClearableFileInput, required=False)

        test_form = TestForm({}, {"test": SimpleUploadedFile("test.txt", b"test")})
        self.assertHTMLEqual(
            render_template_with_bootstrap("{% bootstrap_field form.test %}", context={"form": test_form}),
            (
                '<div class="django_bootstrap5-bound mb-3">'
                '<label class="form-label" for="id_test">Test</label>'
                '<input type="file" name="test" class="form-control django_bootstrap5-bound" id="id_test">'
                "</div>"
            ),
        )


class FieldTest(TestCase):
    def _select_one_element(self, html, selector, err_msg):
        """
        Select exactly one html element in an BeautifulSoup html fragment.

        Fail if there is not exactly one element.
        """
        lst = html.select(selector)
        self.assertEqual(len(lst), 1, err_msg)
        return lst[0]

    def test_illegal_field(self):
        with self.assertRaises(BootstrapError):
            render_field(field="illegal")

    def test_show_help(self):
        html = render_form_field("subject")
        self.assertIn("my_help_text", html)
        self.assertNotIn("<i>my_help_text</i>", html)
        html = render_template_with_form("{% bootstrap_field form.subject show_help=0 %}")
        self.assertNotIn("my_help_text", html)

    def test_subject(self):
        res = render_form_field("subject")
        self.assertIn('type="text"', res)
        self.assertIn('placeholder="placeholdertest"', res)

    def test_xss_field(self):
        html = render_form_field("xss_field")
        self.assertIn('type="text"', html)
        self.assertIn(html_39x27(">XSS&quot; onmouseover=&quot;alert(&#x27;Hello, XSS&#x27;)&quot; foo=&quot;<"), html)
        self.assertIn(
            html_39x27('placeholder="XSS&quot; onmouseover=&quot;alert(&#x27;Hello, XSS&#x27;)&quot; foo=&quot;"'), html
        )

    def test_password(self):
        res = render_form_field("password")
        self.assertIn('type="password"', res)
        self.assertIn('placeholder="Password"', res)

    # def test_radio_select(self):
    #     """Test RadioSelect rendering, because it is special."""
    #     res = render_form_field("category1")
    #     # strip out newlines and spaces around newlines
    #     res = "".join(line.strip() for line in res.split("\n"))
    #     res = BeautifulSoup(res, "html.parser")
    #     form_group = self._select_one_element(
    #       res,
    #       ".form-group", "RadioSelect should be rendered inside a .form-group")
    #     radio = self._select_one_element(form_group, ".radio", "There should be a .radio inside .form-group")
    #     self.assertIn("radio-success", radio["class"], "The radio select should have the class 'radio-success'")
    #     elements = radio.find_all("div", class_="form-check")
    #     self.assertIsNotNone(elements, "Radio should have at least one div with class 'form-check'")
    #     for idx, form_check in enumerate(elements, start=1):
    #         label = form_check.next_element
    #         self.assertIsNotNone(label, "The label should be rendered after the form-check div")
    #         self.assertEqual(label.name, "label", "After the form-check div there should be a label")
    #         self.assertIn("form-check-label", label["class"], "The label should have the class 'form-check-label'")
    #         self.assertEqual(
    #             "Radio {idx}".format(idx=idx), label.text, "The label should have text 'Radio {idx}'".format(idx=idx)
    #         )
    #         input_ = label.next_element
    #         self.assertIsNotNone(input_, "The input should be rendered after the label")
    #         self.assertEqual(input_.name, "input", "After the label there should be an input")
    #         self.assertIn("form-check-input", input_["class"], "The input should have the class 'form-check-input'")
    #         self.assertEqual(
    #             str(idx),
    #             input_["value"],
    #             "The input should have value '{idx}'".format(idx=idx),
    #         )
    #         self.assertEqual(
    #             label["for"], input_["id"], "The for attribute of the label should be the id of the radio input"
    #         )
    #
    # def test_checkbox(self):
    #     """Test Checkbox rendering, because it is special."""
    #     res = render_form_field("cc_myself")
    #     # strip out newlines and spaces around newlines
    #     res = "".join(line.strip() for line in res.split("\n"))
    #     res = BeautifulSoup(res, "html.parser")
    #     form_group = self._select_one_element(res, ".form-group", "Checkbox should be rendered inside a .form-group.")
    #     form_check = self._select_one_element(
    #         form_group, ".form-check", "There should be a .form-check inside .form-group"
    #     )
    #     checkbox = self._select_one_element(form_check, "input", "The checkbox should be inside the .form-check")
    #     self.assertIn("form-check-input", checkbox["class"], "The checkbox should have the class 'form-check-input'.")
    #     label = checkbox.nextSibling
    #     self.assertIsNotNone(label, "The label should be rendered after the checkbox.")
    #     self.assertEqual(label.name, "label", "After the checkbox there should be a label.")
    #     self.assertEqual(
    #         label["for"], checkbox["id"], "The for attribute of the label should be the id of the checkbox."
    #     )
    #     help_text = label.nextSibling
    #     self.assertIsNotNone(help_text, "The help text should be rendered after the label.")
    #     self.assertEqual(help_text.name, "small", "The help text should be rendered as <small> tag.")
    #     self.assertIn("form-text", help_text["class"], "The help text should have the class 'form-text'.")
    #     self.assertIn("text-muted", help_text["class"], "The help text should have the class 'text-muted'.")

    def test_required_field(self):
        required_css_class = "django_bootstrap5-req"
        required_field = render_form_field("subject")
        self.assertIn(required_css_class, required_field)
        not_required_field = render_form_field("message")
        self.assertNotIn(required_css_class, not_required_field)
        # Required settings in field
        form_field = "form.subject"
        rendered = render_template_with_form(
            "{% bootstrap_field " + form_field + ' required_css_class="test-required" %}'
        )
        self.assertIn("test-required", rendered)

    def test_empty_permitted(self):
        """If a form has empty_permitted, no fields should get the CSS class for required."""
        required_css_class = "django_bootstrap5-req"
        form = TestForm()
        res = render_form_field("subject", {"form": form})
        self.assertIn(required_css_class, res)
        form.empty_permitted = True
        res = render_form_field("subject", {"form": form})
        self.assertNotIn(required_css_class, res)

    # def test_input_group(self):
    #     res = render_template_with_form('{% bootstrap_field form.subject addon_before="$"  addon_after=".00" %}')
    #     self.assertIn('class="input-group"', res)
    #     self.assertIn('class="input-group-prepend"><span class="input-group-text">$', res)
    #     self.assertIn('class="input-group-append"><span class="input-group-text">.00', res)
    #
    # def test_input_group_addon_button(self):
    #     res = render_template_with_form(
    #         # Jumping through hoops to keep flake8 and black happy here
    #         "{% bootstrap_field "
    #         'form.subject addon_before="$" addon_before_class=None addon_after=".00" addon_after_class=None'
    #         " %}"
    #     )
    #     self.assertIn('class="input-group"', res)
    #     self.assertIn('<div class="input-group-prepend">$</div>', res)
    #     self.assertIn('<div class="input-group-append">.00</div>', res)
    #
    # def test_input_group_addon_empty(self):
    #     res = render_template_with_form(
    #         '{% bootstrap_field form.subject addon_before=None addon_after="after" %}'
    #     )  # noqa
    #     self.assertIn('class="input-group"', res)
    #     self.assertNotIn("input-group-prepend", res)
    #     self.assertIn('<div class="input-group-append"><span class="input-group-text">after</span></div>', res)

    # def test_input_group_addon_validation(self):
    #     """
    #     Test that invalid-feedback messages are placed inside input-groups.
    #
    #     See issue #89.
    #     """
    #     # invalid form data:
    #     data = {"subject": ""}
    #     res = render_template_with_form(
    #         '{% bootstrap_field form.subject addon_before=None addon_after="after" %}', data=data
    #     )  # noqa
    #     res = BeautifulSoup(res, "html.parser")
    #     self._select_one_element(
    #         res,
    #         ".input-group > .invalid-feedback",
    #         "The invalid-feedback message, complaining that this field is "
    #         "required, must be placed inside the input-group",
    #     )
    #     self._select_one_element(
    #         res, ".form-group > .form-text", "The form-text message must be placed inside the form-group"
    #     )
    #     self.assertEqual(
    #         len(res.select(".form-group > .invalid-feedback")),
    #         0,
    #         "The invalid-feedback message must be placed inside the " "input-group and not inside the form-group",
    #     )
    #     self.assertEqual(
    #         len(res.select(".input-group > .form-text")),
    #         0,
    #         "The form-text message must be placed inside the form-group and " "not inside the input-group",
    #     )

    def test_size(self):
        def _test_size(param, klass):
            res = render_template_with_form('{% bootstrap_field form.subject size="' + param + '" %}')
            self.assertIn(klass, res)

        def _test_size_medium(param):
            res = render_template_with_form('{% bootstrap_field form.subject size="' + param + '" %}')
            self.assertNotIn("form-control-lg", res)
            self.assertNotIn("form-control-sm", res)
            self.assertNotIn("form-control-md", res)

        _test_size("sm", "form-control-sm")
        _test_size("lg", "form-control-lg")
        _test_size_medium("md")
        _test_size_medium("")

    def test_datetime(self):
        field = render_form_field("datetime")
        self.assertIn("vDateField", field)
        self.assertIn("vTimeField", field)

    def test_field_same_render(self):
        context = dict(form=TestForm())
        rendered_a = render_form_field("addon", context)
        rendered_b = render_form_field("addon", context)
        self.assertEqual(rendered_a, rendered_b)

    def test_label(self):
        res = render_template_with_form('{% bootstrap_label "foobar" label_for="subject" %}')
        self.assertEqual('<label for="subject">foobar</label>', res)

    def test_attributes_consistency(self):
        form = TestForm()
        attrs = form.fields["addon"].widget.attrs.copy()
        self.assertEqual(attrs, form.fields["addon"].widget.attrs)
