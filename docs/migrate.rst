=========
Migration
=========

Below is a list of caveats when migrating from `django-bootstrap4` (Bootstrap 4) to `django-bootstrap5` (Bootstrap 5).

This document only considers the differences between `django-bootstrap4` and `django-bootstrap5`. For the migration
guide from Bootstrap 3 to 4, please look at the Bootstrap docs, especially the `Migration section <https://getbootstrap.com/docs/4.6/migration/>`_.

jQuery
------

Bootstrap 5 does not depend on jQuery. Every function and tag referencing jQuery has been removed.

If you need jQuery, you will have to include it yourself.

Popper
------

We use the Bootstrap 5 JavaScript that has bundled Popper.

If you want a separate Popper.js file, do not use the `{% bootstrap_javascript %}` tag, but load the JavaScript yourself.