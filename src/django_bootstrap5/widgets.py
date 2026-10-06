from django.forms import (
    CheckboxSelectMultiple,
    ClearableFileInput,
    EmailInput,
    NumberInput,
    PasswordInput,
    RadioSelect,
    Textarea,
    TextInput,
    URLInput,
)

try:
    # If Django is set up without a database, importing this widget gives RuntimeError
    from django.contrib.auth.forms import ReadOnlyPasswordHashWidget
except RuntimeError:  # pragma: no cover - only reachable when Django has no database configured
    ReadOnlyPasswordHashWidget = None


# Django's own templates for the widgets whose template this package replaces.
DJANGO_WIDGET_TEMPLATES = frozenset(
    widget_class.template_name for widget_class in (RadioSelect, CheckboxSelectMultiple, ClearableFileInput)
)


class RadioSelectButtonGroup(RadioSelect):
    """A RadioSelect that renders as a horizontal button group."""

    template_name = "django_bootstrap5/widgets/radio_select_button_group.html"


def is_widget_with_placeholder(widget):
    """Return whether this widget can have a placeholder."""
    if isinstance(widget, TextInput):
        return widget.input_type not in ("color", "range")
    return isinstance(widget, (TextInput, Textarea, NumberInput, EmailInput, URLInput, PasswordInput))


def set_widget_template(widget, template_name):
    """Set the template for a widget, unless it carries a template of its own."""
    if widget.template_name in DJANGO_WIDGET_TEMPLATES:
        widget.template_name = template_name
