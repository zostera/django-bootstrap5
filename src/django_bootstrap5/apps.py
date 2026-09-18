"""Application configuration and system checks."""

from django.apps import AppConfig
from django.core.checks import Warning, register

#: Keys that look like settings but are not read by this package, with the hint to show.
#: Names from django-bootstrap3 and django-bootstrap4 are listed because they arrive here
#: when a project carries its old settings dict across.
REMOVED_SETTINGS = {
    "use_i18n": "removed in 0.3.0; it duplicated standard Django functionality",
    "base_url": "not a django-bootstrap5 setting; use `css_url` and `javascript_url`",
    "include_jquery": "not a django-bootstrap5 setting; Bootstrap 5 does not use jQuery",
    "jquery_url": "not a django-bootstrap5 setting; Bootstrap 5 does not use jQuery",
}


@register()
def check_bootstrap5_settings(app_configs, **kwargs):
    """Warn about keys in the BOOTSTRAP5 setting that this package never reads."""
    from django.conf import settings

    from django_bootstrap5.core import BOOTSTRAP5_DEFAULTS

    warnings = []
    for key in getattr(settings, "BOOTSTRAP5", {}):
        if key in BOOTSTRAP5_DEFAULTS:
            continue
        hint = REMOVED_SETTINGS.get(key, "not a django-bootstrap5 setting; it is ignored")
        warnings.append(
            Warning(
                f"BOOTSTRAP5[{key!r}] has no effect: {hint}.",
                id="django_bootstrap5.W001",
            )
        )
    return warnings


class DjangoBootstrap5Config(AppConfig):
    """Default application configuration."""

    name = "django_bootstrap5"
