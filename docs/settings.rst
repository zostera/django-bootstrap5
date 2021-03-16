========
Settings
========

The django-bootstrap5 has some pre-configured settings.

They can be modified by adding a dict variable called ``BOOTSTRAP5`` in your ``settings.py`` and customizing the values ​​you want;

The ``BOOTSTRAP5`` dict variable contains these settings and defaults:


.. code:: django

    # Default settings
    BOOTSTRAP5 = {

        # The complete URL to the Bootstrap CSS file
        # Note that a URL can be either a string,
        # e.g. "https://stackpath.bootstrapcdn.com/bootstrap/4.1.1/css/bootstrap.min.css",
        # or a dict like the default value below.
        "css_url": {
            "url": "https://cdn.jsdelivr.net/npm/bootstrap@4.6.0/dist/css/bootstrap.min.css",
            "integrity": "sha384-B0vP5xmATw1+K9KRQjQERJvTumQW0nPEzvF6L/Z6nronJ3oUOFUFpCjEUQouq2+l",
            "crossorigin": "anonymous",
        },

        # The complete URL to the Bootstrap bundle JavaScript file
        "javascript_url": {
            "url": "https://cdn.jsdelivr.net/npm/bootstrap@4.6.0/dist/js/bootstrap.bundle.min.js",
            "integrity": "sha384-Piv4xVNRyMGpqkS2by6br4gNJ7DXjqk09RmUpJ8jgGtD7zP9yug3goQfGII0yAns",
            "crossorigin": "anonymous",
        },

        # The complete URL to the Bootstrap CSS theme file (None means no theme)
        "theme_url": None,

        # Put JavaScript in the HEAD section of the HTML document (only relevant if you use bootstrap5.html)
        'javascript_in_head': False,

        # Label class to use in horizontal forms
        'horizontal_label_class': 'col-md-3',

        # Field class to use in horizontal forms
        'horizontal_field_class': 'col-md-9',

        # Set placeholder attributes to label if no placeholder is provided
        'set_placeholder': True,

        # Class to indicate required (better to set this in your Django form)
        'required_css_class': '',

        # Class to indicate error (better to set this in your Django form)
        'error_css_class': 'is-invalid',

        # Class to indicate success, meaning the field has valid input (better to set this in your Django form)
        'success_css_class': 'is-valid',

        # Renderers (only set these if you have studied the source and understand the inner workings)
        'formset_renderers':{
            'default': 'django_bootstrap5.renderers.FormsetRenderer',
        },
        'form_renderers': {
            'default': 'django_bootstrap5.renderers.FormRenderer',
        },
        'field_renderers': {
            'default': 'django_bootstrap5.renderers.FieldRenderer',
            'inline': 'django_bootstrap5.renderers.InlineFieldRenderer',
        },
    }
