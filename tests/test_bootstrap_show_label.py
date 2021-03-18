from django.forms import formset_factory
from django.test import TestCase

from tests.base import TestForm, render_template_with_form


class ShowLabelTest(TestCase):
    def test_show_label_false(self):
        form = TestForm()
        res = render_template_with_form("{% bootstrap_form form show_label=False %}", {"form": form})
        self.assertIn("visually-hidden", res)

    def test_show_label_sr_only(self):
        form = TestForm()
        res = render_template_with_form("{% bootstrap_form form show_label='' %}", {"form": form})
        self.assertIn("visually-hidden", res)

    def test_show_label_skip(self):
        form = TestForm()
        res = render_template_with_form("{% bootstrap_form form show_label='skip' %}", {"form": form})
        self.assertNotIn("<label>", res)

    def test_for_formset(self):
        TestFormSet = formset_factory(TestForm, extra=1)
        test_formset = TestFormSet()
        res = render_template_with_form("{% bootstrap_formset formset show_label=False %}", {"formset": test_formset})
        self.assertIn("visually-hidden", res)
