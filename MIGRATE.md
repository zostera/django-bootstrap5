# Migration Guide

This guide covers moving to `django-bootstrap5` from `django-bootstrap3` or from `django-bootstrap4`. It only covers
the differences between the packages. For changes in Bootstrap itself, see the Bootstrap migration guides from
[3 to 4](https://getbootstrap.com/docs/4.6/migration/) and from [4 to 5](https://getbootstrap.com/docs/5.3/migration/).

## From django-bootstrap3

Most projects still on Bootstrap 3 go straight to Bootstrap 5. This section lists what changes in the package on the
way. It is based on a real migration of about 260 templates, so it leads with what took the most work.

### Rename the app, the tags and the templates

- `bootstrap3` becomes `django_bootstrap5` in `INSTALLED_APPS`.
- `{% load bootstrap3 %}` becomes `{% load django_bootstrap5 %}`.
- The `BOOTSTRAP3` setting becomes `BOOTSTRAP5`.
- `bootstrap3/bootstrap3.html` becomes `django_bootstrap5/bootstrap5.html`, and its blocks `bootstrap3_title`,
  `bootstrap3_extra_head`, `bootstrap3_content` and `bootstrap3_extra_script` become `bootstrap5_*`. There are two new
  blocks, `bootstrap5_before_content` and `bootstrap5_after_content`.

### Settings

These keep their name: `css_url`, `javascript_url`, `theme_url`, `javascript_in_head`, `set_placeholder`,
`required_css_class` and `error_css_class`. The rest changes.

| `BOOTSTRAP3` | `BOOTSTRAP5` |
|---|---|
| `jquery_url`, `include_jquery` | Removed. Bootstrap 5 does not use jQuery; load it yourself if you need it. |
| `base_url` (older django-bootstrap3 releases) | Removed. Use `css_url` and `javascript_url`. |
| `success_css_class`, default `"has-success"` | Default `""`. Valid and invalid fields are now marked by `server_side_validation`, default `True`. If you set `success_css_class` to `""` to avoid green fields, set `server_side_validation` to `False`. |
| `horizontal_label_class`, default `"col-md-3"` | Default `"col-sm-2"` |
| `horizontal_field_class`, default `"col-md-9"` | Default `"col-sm-10"` |

**The horizontal defaults change silently.** Every form with `layout="horizontal"` gets different column widths unless
you set the old values in `BOOTSTRAP5`.

New settings include `wrapper_class` (default `"mb-3"`), `horizontal_field_offset_class`, `color_mode`,
`checkbox_layout`, `checkbox_style` and the `inline_*` classes. See {doc}`settings`.

A system check, `django_bootstrap5.W001`, warns about keys in `BOOTSTRAP5` that the package does not read, which
catches settings carried over from `BOOTSTRAP3`.

**Delete the `BOOTSTRAP3` block once you have a `BOOTSTRAP5` one.** `W001` only inspects `BOOTSTRAP5`, so a leftover
block is invisible to it while still reading like live configuration. In one project it sat directly above the working
`BOOTSTRAP5` block, with `jquery_url` naming the same file that a `<script>` tag in the base template loaded directly.
Nothing read the setting any more, but it was the first place anyone looked to find out how jQuery reached the page.

### Removed template tags and filters

#### buttons

`{% buttons %} ... {% endbuttons %}` is gone. `{% bootstrap_button %}` renders a button, but not the wrapper that
`buttons` added, so write that yourself and match it to the form's layout.

For a form with the default layout:

```html
<div class="mb-3">
  {% bootstrap_button "Save" button_type="submit" button_class="btn-primary" %}
</div>
```

For a form with `layout="horizontal"`, use the same offset as the form, which is `horizontal_field_offset_class`
(default `offset-sm-2`) next to `horizontal_field_class` (default `col-sm-10`):

```html
<div class="row mb-3">
  <div class="col-sm-10 offset-sm-2">
    {% bootstrap_button "Save" button_type="submit" button_class="btn-primary" %}
  </div>
</div>
```

Using the horizontal markup under a form with the default layout is an easy mistake when replacing many of these at
once, and it shifts the buttons away from the fields.

#### bootstrap_icon

Removed: Bootstrap 5 has no icon font. Use [django-icons](https://github.com/zostera/django-icons) or Bootstrap Icons.

#### bootstrap_jquery_url

Removed, together with jQuery.

#### bootstrap_message_classes

Replaced by the `bootstrap_message_alert_type` filter, which returns only the alert type, such as `info`, and leaves
`extra_tags` out. Where you can, use `{% bootstrap_messages %}`, which handles both. A template that renders messages
itself passes the extra tags separately, as the package's own `messages.html` does:

```html
{% for message in messages %}
  {% bootstrap_alert message.message alert_type=message|bootstrap_message_alert_type extra_classes=message.extra_tags %}
{% endfor %}
```

### Changed template tag arguments

- `size="small"` and `size="large"` raise `ValueError`. Use `sm` and `lg`.
- `form_group_class` is now `wrapper_class`.
- `bound_css_class` is now `success_css_class`.

**Arguments the package does not know are ignored without a warning.** A `form_group_class` left over from Bootstrap 3
does nothing, so search your templates for the old names.

### Forms

`layout="horizontal"` builds the grid itself. The `form-horizontal` class on `<form>`, which Bootstrap 3 needed next to
it, no longer exists and can go. `layout="inline"` still exists.

### jQuery

Bootstrap 5 does not use jQuery. This package has no `jquery_url` setting and no `{% bootstrap_jquery %}` or
`{% bootstrap_jquery_url %}` tag, so load jQuery from your own template if your code needs it.

For most projects that is all it is, because `include_jquery` defaulted to `False` and the jQuery on the page was
already yours. Where it matters is `jquery_url`, whose default was the unversioned `//code.jquery.com/jquery.min.js`.
That alias still serves jQuery 1.11.1, released in 2014, and is not updated, so a project on the default has been
serving 1.11.1 rather than anything recent. Bootstrap 3 itself accepted `1.9.1 - 3`, so nothing about Bootstrap 3 held
you there, only the default.

Choosing the version yourself is therefore likely to be a jump of two majors. Read jQuery's
[upgrade guide](https://jquery.com/upgrade-guide/) rather than assuming the code still runs, and check your plugins at
the same time, since an old jQuery tends to come with old plugins. One project had to take bootstrap-datepicker from
1.6.0 to 1.10.0 before it ran.

### Bootstrap's own class changes

Not part of this package, but they are most of the work in templates. The ones that came up most:

| Bootstrap 3 | Bootstrap 5 |
|---|---|
| `label label-*` | `badge text-bg-*` |
| `btn-default`, `btn-xs` | for example `btn-outline-secondary`, `btn-sm` |
| `panel` | `card` |
| `pull-right`, `pull-left` | `float-end`, `float-start` |
| `text-left`, `text-right` | `text-start`, `text-end` |
| `hidden`, `hidden-xs`, `visible-xs` | `d-none` and the responsive `d-*` classes |
| `table-condensed` | `table-sm` |
| `col-xs-*` | `col-*` |
| `data-toggle`, `data-target`, `data-dismiss` | `data-bs-toggle`, `data-bs-target`, `data-bs-dismiss` |

Navbars, tabs (`nav-item` and `nav-link`), dropdowns (`dropdown-item`) and pagination (`page-item` and `page-link`)
also need their markup updated. Templates that build Bootstrap markup in JavaScript need the same changes.

## From django-bootstrap4

### Replace references to django app from `bootstrap4` to `django_bootstrap5`

- INSTALLED_APPS in settings.py
- when loading :doc:`templatetags`
- when extending :doc:`templates`
- when using :doc:`widgets`

### Removed templatetags

#### buttons

The `{% buttons %} ... {% endbuttons %}` tag has been removed. To create buttons, use the `{% bootstrap_button %}` tag.

### jQuery

Bootstrap 5 does not depend on jQuery. Every function and tag referencing jQuery has been removed.

If you need jQuery, you will have to include it yourself. django-bootstrap4 defaulted to jQuery 3.5.1, so there is no
major jQuery upgrade in this move, only the loading.

### Popper

We use the bundled version of Bootstrap 5 JavaScript that includes Popper.

If you need a separate Popper.js file, do not use the `{% bootstrap_javascript %}` tag, but load the JavaScript yourself.
