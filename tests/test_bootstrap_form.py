from bs4 import BeautifulSoup
from django.test import TestCase

from django_bootstrap5.exceptions import BootstrapError
from tests.base import TestForm, render_form, render_template_with_form


class BootstrapFormTest(TestCase):
    def test_illegal_form(self):
        with self.assertRaises(BootstrapError):
            render_form(form="illegal")

    def test_field_names(self):
        form = TestForm()
        res = render_form(form)
        for field in form:
            # datetime has a multiwidget field widget
            if field.name == "datetime":
                self.assertIn('name="datetime_0"', res)
                self.assertIn('name="datetime_1"', res)
            else:
                self.assertIn('name="%s"' % field.name, res)

    def test_exclude(self):
        form = TestForm()
        res = render_template_with_form('{% bootstrap_form form exclude="cc_myself" %}', {"form": form})
        self.assertNotIn("cc_myself", res)

    def test_error_class(self):
        form = TestForm({"sender": "sender"})
        res = render_template_with_form("{% bootstrap_form form %}", {"form": form})
        self.assertIn("django_bootstrap5-err", res)

        res = render_template_with_form('{% bootstrap_form form error_css_class="successful-test" %}', {"form": form})
        self.assertIn("successful-test", res)

        res = render_template_with_form('{% bootstrap_form form error_css_class="" %}', {"form": form})
        self.assertNotIn("django_bootstrap5-err", res)

    def test_required_class(self):
        form = TestForm({"sender": "sender"})
        res = render_template_with_form("{% bootstrap_form form %}", {"form": form})
        self.assertIn("django_bootstrap5-req", res)

        res = render_template_with_form(
            '{% bootstrap_form form required_css_class="successful-test" %}', {"form": form}
        )
        self.assertIn("successful-test", res)

        res = render_template_with_form('{% bootstrap_form form required_css_class="" %}', {"form": form})
        self.assertNotIn("django_bootstrap5-req", res)

    def test_bound_class(self):
        form = TestForm({"sender": "sender"})

        res = render_template_with_form("{% bootstrap_form form %}", {"form": form})
        self.assertIn("django_bootstrap5-bound", res)

        form = TestForm({"sender": "sender"})

        res = render_template_with_form('{% bootstrap_form form bound_css_class="successful-test" %}', {"form": form})
        self.assertIn("successful-test", res)

        form = TestForm({"sender": "sender"})

        res = render_template_with_form('{% bootstrap_form form bound_css_class="" %}', {"form": form})
        self.assertNotIn("django_bootstrap5-bound", res)

    # def test_radio_select_button_group(self):
    #     form = TestForm()
    #     res = render_template_with_form("{% bootstrap_form form %}", {"form": form})
    #     self.assertIn('input id="id_category5_0_0" name="category5" required="" type="radio"', res)

    def test_alert_error_type(self):
        form = TestForm({"sender": "sender"})

        # Show all error messages
        res = render_template_with_form("{% bootstrap_form form alert_error_type='all' %}", {"form": form})
        html = BeautifulSoup(res, "html.parser")
        errors = list(html.select(".text-danger")[0].stripped_strings)
        self.assertIn(form.non_field_error_message, errors)
        self.assertIn("This field is required.", errors)

        # Show only non-field error messages (default config)
        res = render_template_with_form("{% bootstrap_form form alert_error_type='non_fields' %}", {"form": form})
        default = render_template_with_form("{% bootstrap_form form %}", {"form": form})
        self.assertEqual(res, default, "Default behavior is not the same as showing non-field errors")
        html = BeautifulSoup(res, "html.parser")
        errors = list(html.select(".text-danger")[0].stripped_strings)
        self.assertIn(form.non_field_error_message, errors)
        self.assertNotIn("This field is required.", errors)

        # Show only field error messages
        res = render_template_with_form("{% bootstrap_form form alert_error_type='fields' %}", {"form": form})
        html = BeautifulSoup(res, "html.parser")
        errors = list(html.select(".text-danger")[0].stripped_strings)
        self.assertNotIn(form.non_field_error_message, errors)
        self.assertIn("This field is required.", errors)

        # Show nothing
        res = render_template_with_form("{% bootstrap_form form alert_error_type='none' %}", {"form": form})
        html = BeautifulSoup(res, "html.parser")
        self.assertFalse(html.select(".text-danger"))
