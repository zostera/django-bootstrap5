=======
Widgets
=======

A form widget is available for displaying radio buttons as a Bootstrap 5 button group(https://getbootstrap.com/docs/4.5/components/button-group/).


RadioSelectButtonGroup
~~~~~~~~~~~~~~~~~~~~~~

*Known issue: This widget currently renders as a regular Bootstrap 5 RadioSelect.*

This renders a form ChoiceField as a Bootstrap 5 button group in the `primary` Bootstrap 5 color.

.. code:: django

    from django_bootstrap5.widgets import RadioSelectButtonGroup

    class MyForm(forms.Form):
        media_type = forms.ChoiceField(
            help_text="Select the order type.",
            required=True,
            label="Order Type:",
            widget=RadioSelectButtonGroup,
            choices=((1, 'Vinyl'), (2, 'Compact Disc')),
            initial=1,
        )
