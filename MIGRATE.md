# Migration Guide

Below is a list of warnings when migrating from `django-bootstrap4` (Bootstrap 4) to `django-bootstrap5` (Bootstrap 5).

This document only considers the differences between `django-bootstrap4` and `django-bootstrap5`. For the migration
guide from Bootstrap 3 to 4, please look at the Bootstrap docs, especially the `Migration section <https://getbootstrap.com/docs/4.6/migration/>`_.

## Replace references to django app from `bootstrap4` to `django_bootstrap5`

- INSTALLED_APPS in settings.py
- when loading :doc:`templatetags`
- when extending :doc:`templates`
- when using :doc:`widgets`

## Removed templatetags

### buttons

The `{% buttons %} ... {% endbuttons %}` tag has been removed. To create buttons, use the `{% bootstrap_button %}` tag.

## jQuery

Bootstrap 5 does not depend on jQuery. Every function and tag referencing jQuery has been removed.

If you need jQuery, you will have to include it yourself.

## Popper

We use the bundled version of Bootstrap 5 JavaScript that includes Popper.

If you need a separate Popper.js file, do not use the `{% bootstrap_javascript %}` tag, but load the JavaScript yourself.
