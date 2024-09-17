# Changelog

## 24.3 (2024-09-17)

- Add support for Django 5.1 (#663).
- Add support for Jinja 2(#664, @jorenham)

## 24.2 (2024-04-23)

- Add .editorconfig (#598).
- Remove support for Django 4.1 (EOL) (#597).
- Add support for color mode (#593).
- Change bootstrap_setting from filter to tag (#595).
- Remove support for Python 3.7 (EOL) (#588).
- Remove support for Django 3.2 (EOL) (#583).
- Update Bootstrap to 5.3.3 (#584).
- Fix Read the Docs (#585, #587).

## 24.1 (2024-04-12)

- Fix RadioSelectButtonGroup rendering and add 'disabled' attribute to radio button group template (#447).

## 23.4 (2023-12-28)

- Use ruff instead of black for formatting (#536).
- Drop support for Python 3.7 in test matrix (#533).
- Fix support for Django 4.2 in test matrix (#533).
- Pass "horizontal_field_offset_class" to child renderers (#391, #521).
- Add support for Django 5.0 (#538).
- Add support for Python 3.12 (#538).
- Revert packaging tools to setuptools, build, tox and twine (#538).

## 23.3 (2023-06-03)

- Switch to Hatch for builds and environments (#515).
- Improve and fix CI on GitHub Actions (#515).
- Reinstate coveralls (#515).
- Update Sphinx and switch to Furo theme (#515).

## 23.2 (2023-04-29)

- Update packaging, reduce dependencies (#487, #488, #494).
- Drop support for Django 4.0 (#494).
- Add support for Django 4.2 (#480).
- User ruff for linting and formatting (#482).
- Move version to setup.cfg (#487).

## 23.1 (2023-04-02)

- Fix documentation for button sizes (#457).
- Update Bootstrap to 5.2.3 (#393).
- Updated requirements and packages (#458).
- Stop using coveralls service (#459).

## 22.2 (2022-11-22)

- Add support for Python 3.11 (#389).
- Make it easier to override templates in custom renderers (#373).
- Added `.form-label` default to `<label>` tags (#180).
- Update radio_select_button_group widget to BS5 (#313).
- Fix `addon_before_class` and `addon_after_class`, which were being ignored (#153).
- Fix to issue (#349) where `has-validation` was incorrectly rounding before and after elements' borders when validated.
- Update the default JS and CSS urls mentioned on the settings page of the documentation.

## 22.1 (2022-08-08)

- Update Bootstrap to 5.2.0 (#325).
- Add support for Django 4.1 (#322).
- Drop support for Django 2.2 (EOL) (#324).

## 21.3 (2021-12-27)

- Drop support for Python 3.6 (EOL, #247, #248).
- Drop support for Django 3.1 (EOL, #247, #248).
- Fix tests for Django 4.1 (#247).
- Update example app (#250).

## 21.2 (2021-12-12)

- Fix typo in Bootstrap JavaScript url (#209, #204).
- Add test to validate Bootstrap urls (#225).

## 21.1 (2021-11-01)

- Switch to a [CalVer](https://calver.org) YY.MINOR versioning scheme. MINOR is the number of the release in the given year. This is the first release in 2021 using this scheme, so its version is 21.1. The next version this year will be 21.2. The first version in 2022 will be 22.1.
- Update Bootstrap to 5.1.3 (#167, #194).
- Add support for Django 4 and Python 3.10 (#193).

## 2.1.2 (2021-08-16)

- Fix disabled parameter for RadioSelect and CheckboxSelectMultiple (#163).

## 2.1.1 (2021-07-11)

- Respect safe strings in bootstrap_messages (#145).

## 2.1.0 (2021-07-11)

- Bump Bootstrap from 5.0.1 to 5.0.2 (#138).

## 2.0.1 (2021-06-11)

- Fix bug in exclude handling (#124).

## 2.0.0 (2021-05-16)

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

## 1.0.0 (2021-04-30)

- Set PyPI classifier "Development Status :: 5 - Production/Stable".
- Support addons for `form-control` widgets.

## 0.6.0 (2021-04-26)

- Add support for floating labels on input types `date`, `time`, `url`, `email`, `tel`.
- Improve code coverage and tests.

## 0.5.0 (2021-04-23)

- Fix pagination support.

## 0.4.0 (2021-04-20)

- Refactor tests.
- Add support for input "range".
- Add support for input "color".
- Add support for floating labels on `Select` widgets.

## 0.3.0 (2021-04-18)

- Fix suport for `Textarea` widgets.
- Add support for horizontal forms.
- Add support for `checkbox_type="switch"`.
- Set PyPI Development Status to 4 - Beta.
- Remove use_i18n setting because it duplicates standard Django functionality.
- Update Bootstrap to 5.0.0-beta3
- Remove `buttons` tag.
- Drop support for Django 3.0, extended support stopped on 2021-04-01).
- Add support for Django 3.2.

## 0.2.0 (2021-03-22)

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

## 0.1.0 (2013-08-13)

- Reserving the name "django-bootstrap5" at PyPI (released as 0.1).
