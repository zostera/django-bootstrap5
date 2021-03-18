# django-bootstrap5

[![CI](https://github.com/zostera/django-bootstrap5/workflows/CI/badge.svg?branch=main)](https://github.com/zostera/django-bootstrap5/actions?workflow=CI)
[![Coverage Status](https://coveralls.io/repos/github/zostera/django-bootstrap5/badge.svg?branch=main)](https://coveralls.io/github/zostera/django-bootstrap5?branch=main)
[![Latest PyPI version](https://img.shields.io/pypi/v/django-bootstrap5.svg)](https://pypi.python.org/pypi/django-bootstrap5)
[![Any color you like](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

Bootstrap 5 for Django.

## Goal

The goal of this project is to seamlessly blend Django and Bootstrap 5.

## Status

Early development, not ready for production. Issues and pull requests welcome.

## Requirements

Python 3.6 or newer with Django >= 2.2 or newer.

## Documentation

The full documentation is at https://django-bootstrap5.readthedocs.io/

## Installation

1. Install using pip:

    ```shell script
    pip install django-bootstrap5
    ```
   
   Alternatively, you can install download or clone this repo and call ``pip install -e .``.

2. Add to `INSTALLED_APPS` in your `settings.py`:

   ```python
   INSTALLED_APPS = (
       # ...
       "django_bootstrap5",
       # ...
   )
   ````

3. In your templates, load the `django_bootstrap5` library and use the `bootstrap_*` tags:

## Example template

```djangotemplate
{% load django_bootstrap5 %}

{# Display a form #}

<form action="/url/to/submit/" method="post" class="form">
    {% csrf_token %}
    {% bootstrap_form form %}
    {% buttons %}
        <button type="submit" class="btn btn-primary">Submit</button>
    {% endbuttons %}
</form>
```

Demo
----

A demo app is provided in `demo`. You can run it from your virtualenv with `python manage.py runserver`.


Bugs and suggestions
--------------------

If you have found a bug or if you have a request for additional functionality, please use the issue tracker on GitHub.

https://github.com/zostera/django-bootstrap5/issues


License
-------

You can use this under BSD-3-Clause. See [LICENSE](LICENSE) file for details.


Author
------

Developed and maintained by [Zostera](https://zostera.nl).

Original author: [Dylan Verheul](https://github.com/dyve).

Thanks to everybody that has contributed pull requests, ideas, issues, comments and kind words.

Please see [AUTHORS](AUTHORS) for a list of contributors.
