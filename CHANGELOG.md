# Changelog

## [2.1.0] - 2021-07-11

- Bump Bootstrap from 5.0.1 to 5.0.2 (#138).

## [2.0.1] - 2021-06-11

- Fix bug in exclude handling (#124).

## [2.0.0] - 2021-05-16

- Use `wrapper_class` and `inline_wrapper_class` for spacing (#113).
- Document known issue with `RadioSelectButtonGroup` (#114).
- Bump Bootstrap from 5.0.0 to 5.0.1 (#110).
- Fix validation HTML for checkbox and radio select (#92).
- Ignore placeholders in attributes in render_tag (#103). 
- Update default Bootstrap to 5.0.0 (#97).
- Fix issue where error messages were not displayed for input groups.
- Introduce `server_side_validation` setting for controlling Bootstrap 5 server-side validation classes (#90).
- Use `success_css_class` instead of `bound_css_class`.
- Use standard Exception classes (#83).
- Support `extra_classes` in `render_alert` (#81).
- Do not apply `mark_safe` to content for `bootstrap_button`.
- Add keyword arguments to `bootstrap_button` tag (#79).
- Add size parameter to example forms (#77).

## [1.0.0] - 2021-04-30

- Set PyPI classifier "Development Status :: 5 - Production/Stable".
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
