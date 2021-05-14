========
Settings
========

The django-bootstrap5 has some pre-configured settings.

They can be modified by adding a dict variable called ``BOOTSTRAP5`` in your ``settings.py`` and customizing the values ​​you want;

The ``BOOTSTRAP5`` dict variable contains these settings and defaults:


.. code:: django

    # Default settings
    BOOTSTRAP5 = {

        # The complete URL to the Bootstrap CSS file.
        # Note that a URL can be either a string
        # ("https://stackpath.bootstrapcdn.com/bootstrap/4.1.1/css/bootstrap.min.css"),
        # or a dict with keys `url`, `integrity` and `crossorigin` like the default value below.
        "css_url": {
            "url": "https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta2/dist/css/bootstrap.min.css",
            "integrity": "sha384-BmbxuPwQa2lc/FVzBcNJ7UAyJxM6wuqIj61tLrc4wSX0szH/Ev+nYRRuWlolflfl",
            "crossorigin": "anonymous",
        },

        # The complete URL to the Bootstrap bundle JavaScript file.
        "javascript_url": {
            "url": "https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta2/dist/js/bootstrap.bundle.min.js",
            "integrity": "sha384-b5kHyXgcpbZJO/tY9Ul7kGkf1S0CWuKcCD38l8YkeH8z8QjE0GmW1gYU5S9FOnJ0",
            "crossorigin": "anonymous",
        },

        # The complete URL to the Bootstrap CSS theme file (None means no theme).
        "theme_url": None,

        # Put JavaScript in the HEAD section of the HTML document (only relevant if you use bootstrap5.html).
        'javascript_in_head': False,

        # Wrapper class for non-inline fields.
        # The default value "mb-3" is the spacing as used by Bootstrap 5 example code.
        'wrapper_class': 'mb-3',

        # Wrapper class for inline fields.
        # The default value is empty, as Bootstrap5 example code doesn't use a wrapper class.
        'inline_wrapper_class': '',

        # Label class to use in horizontal forms.
        'horizontal_label_class': 'col-sm-2',

        # Field class to use in horizontal forms.
        'horizontal_field_class': 'col-sm-10',

        # Field class used for horizontal fields withut a label.
        'horizontal_field_offset_class': 'offset-sm-2',

        # Set placeholder attributes to label if no placeholder is provided.
        'set_placeholder': True,

        # Class to indicate required field (better to set this in your Django form).
        'required_css_class': '',

        # Class to indicate field has one or more errors (better to set this in your Django form).
        'error_css_class': '',

        # Class to indicate success, meaning the field has valid input (better to set this in your Django form).
        'success_css_class': '',

        # Enable or disable Bootstrap 5 server side validation classes (separate from the indicator classes above).
        'server_side_validation': True,

        # Renderers (only set these if you have studied the source and understand the inner workings).
        'formset_renderers':{
            'default': 'django_bootstrap5.renderers.FormsetRenderer',
        },
        'form_renderers': {
            'default': 'django_bootstrap5.renderers.FormRenderer',
        },
        'field_renderers': {
            'default': 'django_bootstrap5.renderers.FieldRenderer',
        },
    }
