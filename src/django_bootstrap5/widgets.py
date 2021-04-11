from django.forms import EmailInput, NumberInput, PasswordInput, RadioSelect, Textarea, TextInput, URLInput


class RadioSelectButtonGroup(RadioSelect):
    """A RadioSelect that renders as a horizontal button groep."""

    template_name = "django_bootstrap5/widgets/radio_select_button_group.html"


def is_widget_with_placeholder(widget):
    """Return whether this widget can have a placeholder."""
    return isinstance(widget, (TextInput, Textarea, NumberInput, EmailInput, URLInput, PasswordInput))
