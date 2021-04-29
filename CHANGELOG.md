# Changelog

## [1.0.0] - 2021-04-30

- Set PyPI classifier for Development Status to Production/Stable.
- Support addons for `form-control` widgets.

## [0.6.0] - 2021-04-26

- Add support for floating labels on input types `date`, `time`, `url`, `email`, `tel`.
- Improve code coverage and tests.

## [0.5.0] - 2021-04-23

- Fix pagination support.

## [0.4.0] - 2021-04-20

- Refactor tests.
- Add support for input "range".
- Add support for input "color".
- Add support for floating labels on `Select` widgets.

## [0.3.0] - 2021-04-18

- Fix suport for `Textarea` widgets.
- Add support for horizontal forms.
- Add support for `checkbox_type="switch"`.
- Set PyPI Development Status to 4 - Beta.
- Remove use_i18n setting because it duplicates standard Django functionality.
- Update Bootstrap to 5.0.0-beta3
- Remove `buttons` tag.
- Drop support for Django 3.0, extended support stopped on 2021-04-01).
- Add support for Django 3.2.

## [0.2.0] - 2021-03-22

- Add floating labels for supported widgets. 
- Do not abuse title element for help text.
- Remove `InlineFieldRenderer`.
- Simplify size parameters, only accept "sm", "md", "lg".
- Use `bootstrap_alert` in `bootstrap_messages`.
- Document approach to form rendering in `docs/forms.rst`.
- Use .readthedocs.yml to configure Read the Docs.
- Place AUTHORS in text file, remove authors from documentation.
- Drop all jQuery support since Bootstrap 5 does not need jQuery.
- Use `django_bootstrap5` as name for Python package.
- Started `django-bootstrap5` based on `django-bootstrap4`.
- Thanks everybody that contributed to `django-bootstrap4` and earlier versions!

## [0.1.0] - 2013-08-13 

- Reserving the name "django-bootstrap5" at PyPI (released as 0.1). 
