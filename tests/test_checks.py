from django.core.checks import Warning, registry
from django.test import SimpleTestCase

from django_bootstrap5.apps import check_bootstrap5_settings


class CheckBootstrap5SettingsTestCase(SimpleTestCase):
    def test_registered(self):
        """The check runs as part of manage.py check."""
        self.assertIn(check_bootstrap5_settings, registry.registry.get_checks())

    def test_known_settings_are_silent(self):
        with self.settings(BOOTSTRAP5={"wrapper_class": "mb-4", "inline_field_class": "col-auto"}):
            self.assertEqual(check_bootstrap5_settings(None), [])

    def test_empty_settings_are_silent(self):
        with self.settings(BOOTSTRAP5={}):
            self.assertEqual(check_bootstrap5_settings(None), [])

    def test_every_default_is_accepted(self):
        """No default key warns about itself."""
        from django_bootstrap5.core import BOOTSTRAP5_DEFAULTS

        with self.settings(BOOTSTRAP5=dict(BOOTSTRAP5_DEFAULTS)):
            self.assertEqual(check_bootstrap5_settings(None), [])

    def test_unknown_key_warns(self):
        with self.settings(BOOTSTRAP5={"no_such_setting": "value"}):
            warnings = check_bootstrap5_settings(None)
        self.assertEqual(len(warnings), 1)
        self.assertIsInstance(warnings[0], Warning)
        self.assertEqual(warnings[0].id, "django_bootstrap5.W001")
        self.assertEqual(
            warnings[0].msg,
            "BOOTSTRAP5['no_such_setting'] has no effect: not a django-bootstrap5 setting; it is ignored.",
        )

    def test_removed_setting_warns_with_its_own_hint(self):
        with self.settings(BOOTSTRAP5={"use_i18n": True}):
            warnings = check_bootstrap5_settings(None)
        self.assertEqual(len(warnings), 1)
        self.assertEqual(
            warnings[0].msg,
            "BOOTSTRAP5['use_i18n'] has no effect: removed in 0.3.0; it duplicated standard Django functionality.",
        )

    def test_jquery_settings_carried_over_from_bootstrap3_or_4_warn(self):
        with self.settings(BOOTSTRAP5={"include_jquery": True, "jquery_url": "jquery.js"}):
            warnings = check_bootstrap5_settings(None)
        self.assertEqual(len(warnings), 2)
        for warning in warnings:
            self.assertIn("Bootstrap 5 does not use jQuery", warning.msg)

    def test_one_warning_per_unknown_key(self):
        with self.settings(BOOTSTRAP5={"wrapper_class": "mb-4", "base_url": "/static/", "nope": 1}):
            warnings = check_bootstrap5_settings(None)
        self.assertEqual(len(warnings), 2)
        self.assertIn("base_url", warnings[0].msg)
        self.assertIn("use `css_url` and `javascript_url`", warnings[0].msg)
        self.assertIn("nope", warnings[1].msg)
