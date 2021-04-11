from django.forms import EmailInput, NumberInput, PasswordInput, RadioSelect, Textarea, TextInput, URLInput


class RadioSelectButtonGroup(RadioSelect):
    """
    This widget renders a Bootstrap 5 set of buttons horizontally instead of typical radio buttons.

    Much more mobile friendly.
    """

    template_name = "django_bootstrap5/widgets/radio_select_button_group.html"


def is_widget_with_placeholder(widget):
    """
    Return whether this widget should have a placeholder.

    Only text, text area, number, e-mail, url, password, number and derived inputs have placeholders.
    """
    return isinstance(widget, (TextInput, Textarea, NumberInput, EmailInput, URLInput, PasswordInput))
