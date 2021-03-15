from django.forms import RadioSelect


class RadioSelectButtonGroup(RadioSelect):
    """
    This widget renders a Bootstrap 5 set of buttons horizontally instead of typical radio buttons.

    Much more mobile friendly.
    """

    template_name = "django_bootstrap5/widgets/radio_select_button_group.html"
