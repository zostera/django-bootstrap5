from django import forms
from django.forms import formset_factory

from tests.base import BootstrapTestCase


class TestForm(forms.Form):
    subject = forms.CharField()


class LabelTestCase(BootstrapTestCase):
    def test_show_label_false(self):
        self.assertInHTML(
            '<label class="visually-hidden" for="id_subject">Subject</label>',
            self.render("{% bootstrap_form form show_label=False %}", {"form": TestForm()}),
        )

    def test_show_label_sr_only(self):
        self.assertInHTML(
            '<label class="visually-hidden" for="id_subject">Subject</label>',
            self.render("{% bootstrap_form form show_label='' %}", {"form": TestForm()}),
        )

    def test_show_label_skip(self):
        self.assertNotIn(
            "label",
            self.render("{% bootstrap_form form show_label='skip' %}", {"form": TestForm()}),
        )

    def test_show_label_false_in_formset(self):
        TestFormSet = formset_factory(TestForm, extra=1)
        self.assertInHTML(
            '<label class="visually-hidden" for="id_form-0-subject">Subject</label>',
            self.render("{% bootstrap_formset formset show_label=False %}", {"formset": TestFormSet()}),
        )
