"""Tests for code paths that the feature-oriented test files do not reach."""

from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashWidget
from django.forms import formset_factory

from django_bootstrap5.core import get_bootstrap_setting
from django_bootstrap5.renderers import BaseRenderer
from django_bootstrap5.templatetags.django_bootstrap5 import bootstrap_server_side_validation_class
from tests.base import BootstrapTestCase


class HiddenFieldForm(forms.Form):
    hidden = forms.CharField(widget=forms.HiddenInput, required=False)


class CheckboxForm(forms.Form):
    agree = forms.BooleanField(required=False)


class PlaintextForm(forms.Form):
    password = forms.CharField(widget=ReadOnlyPasswordHashWidget)


class SizedForm(forms.Form):
    name = forms.CharField()


class RequiredForm(forms.Form):
    name = forms.CharField()


class ComplainingFormSet(forms.BaseFormSet):
    def clean(self):
        raise forms.ValidationError("Formset-level problem.")


class BaseRendererTestCase(BootstrapTestCase):
    def test_render_returns_empty_html(self):
        """BaseRenderer.render is a no-op that subclasses override."""
        self.assertEqual(BaseRenderer().render(), "")


class HiddenFieldTestCase(BootstrapTestCase):
    def test_hidden_field_renders_widget_only(self):
        html = self.render("{% bootstrap_field form.hidden %}", {"form": HiddenFieldForm()})
        self.assertIn('type="hidden"', html)
        self.assertNotIn("form-label", html)
        self.assertNotIn("mb-3", html)


class CheckboxLayoutTestCase(BootstrapTestCase):
    def test_checkbox_layout_inline_adds_form_check_inline(self):
        html = self.render('{% bootstrap_field form.agree checkbox_layout="inline" %}', {"form": CheckboxForm()})
        self.assertIn("form-check-inline", html)

    def test_checkbox_style_switch_adds_form_switch(self):
        html = self.render('{% bootstrap_field form.agree checkbox_style="switch" %}', {"form": CheckboxForm()})
        self.assertIn("form-switch", html)


class ReadOnlyPasswordHashTestCase(BootstrapTestCase):
    def test_read_only_password_hash_widget_gets_plaintext_class(self):
        html = self.render("{% bootstrap_field form.password %}", {"form": PlaintextForm()})
        self.assertIn("form-control-plaintext", html)


class SizeClassTestCase(BootstrapTestCase):
    def test_size_small_and_large_add_a_size_class(self):
        for size, expected in (("sm", "form-control-sm"), ("lg", "form-control-lg")):
            with self.subTest(size=size):
                template = '{% bootstrap_field form.name size="' + size + '" %}'
                html = self.render(template, {"form": SizedForm()})
                self.assertIn(expected, html)

    def test_default_size_adds_no_size_class(self):
        html = self.render("{% bootstrap_field form.name %}", {"form": SizedForm()})
        self.assertNotIn("form-control-sm", html)
        self.assertNotIn("form-control-lg", html)


class FormsetErrorsTestCase(BootstrapTestCase):
    def test_non_form_errors_are_rendered(self):
        formset_class = formset_factory(RequiredForm, formset=ComplainingFormSet, extra=1)
        formset = formset_class(
            data={
                "form-TOTAL_FORMS": "1",
                "form-INITIAL_FORMS": "0",
                "form-MIN_NUM_FORMS": "0",
                "form-MAX_NUM_FORMS": "1000",
                "form-0-name": "value",
            }
        )
        self.assertFalse(formset.is_valid())
        html = self.render("{% bootstrap_formset formset %}", {"formset": formset})
        self.assertIn("Formset-level problem.", html)


class ServerSideValidationClassTestCase(BootstrapTestCase):
    def test_missing_attrs_returns_empty_string(self):
        """The tag is given a widget dict that carries no class, which must not raise."""
        self.assertEqual(bootstrap_server_side_validation_class({}), "")
        self.assertEqual(bootstrap_server_side_validation_class({"attrs": {}}), "")

    def test_validation_class_is_returned(self):
        self.assertEqual(bootstrap_server_side_validation_class({"attrs": {"class": "is-invalid"}}), "is-invalid")
        self.assertEqual(bootstrap_server_side_validation_class({"attrs": {"class": "is-valid"}}), "is-valid")

    def test_non_validation_class_is_dropped(self):
        self.assertEqual(bootstrap_server_side_validation_class({"attrs": {"class": "form-control"}}), "")

    def test_a_space_separated_class_string_is_not_split(self):
        """
        Known limitation: the helper compares whole entries, it does not split on whitespace.

        This holds today because the renderer leaves only the validation class on the wrapper of a
        RadioSelect, which is the single caller. It would silently return "" if that ever changed.
        """
        widget = {"attrs": {"class": "form-check-input is-invalid"}}
        self.assertEqual(bootstrap_server_side_validation_class(widget), "")


class EmptyUrlSettingsTestCase(BootstrapTestCase):
    def test_bootstrap_javascript_without_url_renders_nothing(self):
        with self.settings(BOOTSTRAP5={"javascript_url": None}):
            self.assertEqual(self.render("{% bootstrap_javascript %}").strip(), "")

    def test_bootstrap_css_renders_theme_url_when_set(self):
        with self.settings(BOOTSTRAP5={"theme_url": "https://example.com/theme.css"}):
            html = self.render("{% bootstrap_css %}")
        self.assertIn("https://example.com/theme.css", html)

    def test_bootstrap_css_without_url_renders_nothing_for_that_tag(self):
        with self.settings(BOOTSTRAP5={"css_url": None, "theme_url": None}):
            self.assertEqual(self.render("{% bootstrap_css %}").strip(), "")
        self.assertIsNone(get_bootstrap_setting("theme_url"))


class LabelClassTestCase(BootstrapTestCase):
    def test_empty_label_class_renders_no_class_attribute(self):
        self.assertHTMLEqual(
            self.render('{% bootstrap_label "Subject" label_class="" %}'),
            "<label>Subject</label>",
        )


class RendererHelperDefaultsTestCase(BootstrapTestCase):
    """The widget argument of these helpers defaults to the renderer's own widget."""

    def _field_renderer(self):
        from django_bootstrap5.renderers import FieldRenderer

        return FieldRenderer(SizedForm()["name"])

    def test_add_widget_class_attrs_defaults_to_own_widget(self):
        renderer = self._field_renderer()
        renderer.widget.attrs.pop("class", None)
        renderer.add_widget_class_attrs()
        self.assertIn("form-control", renderer.widget.attrs["class"])

    def test_add_placeholder_attrs_defaults_to_own_widget(self):
        renderer = self._field_renderer()
        renderer.widget.attrs.pop("placeholder", None)
        renderer.add_placeholder_attrs()
        self.assertEqual(renderer.widget.attrs["placeholder"], "Name")
