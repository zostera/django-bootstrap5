from importlib import import_module

from django.conf import settings

BOOTSTRAP5_DEFAULTS = {
    "css_url": {
        "url": "https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/css/bootstrap.min.css",
        "integrity": "sha384-sRIl4kxILFvY47J16cr9ZwB07vP4J8+LH7qKQnuqkuIAvNWLzeN8tE5YBujZqJLB",
        "crossorigin": "anonymous",
    },
    "javascript_url": {
        "url": "https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/js/bootstrap.bundle.min.js",
        "integrity": "sha384-FKyoEForCGlyvwx9Hj09JcYn3nv7wiPVlz7YYwJrWVcXK/BmnVDxM+D2scQbITxI",
        "crossorigin": "anonymous",
    },
    "theme_url": None,
    "color_mode": None,
    "javascript_in_head": False,
    "layout": "",
    "wrapper_class": "mb-3",
    "inline_wrapper_class": "",
    "label_class": "",
    "horizontal_label_class": "col-sm-2",
    "horizontal_field_class": "col-sm-10",
    "horizontal_field_offset_class": "offset-sm-2",
    "set_placeholder": True,
    "checkbox_layout": None,
    "checkbox_style": None,
    "required_css_class": "",
    "error_css_class": "",
    "success_css_class": "",
    "server_side_validation": True,
    "formset_renderers": {"default": "django_bootstrap5.renderers.FormsetRenderer"},
    "form_renderers": {"default": "django_bootstrap5.renderers.FormRenderer"},
    "field_renderers": {
        "default": "django_bootstrap5.renderers.FieldRenderer",
    },
    "hyphenate_attribute_prefixes": ["data"],
}


def get_bootstrap_setting(name, default=None):
    """
    Read a setting.

    Lookup order is:

    1. Django settings
    2. `django-bootstrap5` defaults
    3. Given default value
    """
    bootstrap5_settings = getattr(settings, "BOOTSTRAP5", {})
    return bootstrap5_settings.get(name, BOOTSTRAP5_DEFAULTS.get(name, default))


def javascript_url():
    """Return the full url to the Bootstrap JavaScript file."""
    return get_bootstrap_setting("javascript_url")


def css_url():
    """Return the full url to the Bootstrap CSS file."""
    return get_bootstrap_setting("css_url")


def theme_url():
    """Return the full url to the theme CSS file."""
    return get_bootstrap_setting("theme_url")


def get_renderer(renderers, **kwargs):
    layout = kwargs.get("layout", "")
    path = renderers.get(layout, renderers["default"])
    mod, cls = path.rsplit(".", 1)
    return getattr(import_module(mod), cls)


def get_formset_renderer(**kwargs):
    renderers = get_bootstrap_setting("formset_renderers")
    return get_renderer(renderers, **kwargs)


def get_form_renderer(**kwargs):
    renderers = get_bootstrap_setting("form_renderers")
    return get_renderer(renderers, **kwargs)


def get_field_renderer(**kwargs):
    renderers = get_bootstrap_setting("field_renderers")
    return get_renderer(renderers, **kwargs)
