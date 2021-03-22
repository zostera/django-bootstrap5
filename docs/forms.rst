=====
Forms
=====

Forms are an important part of any Bootstrap version.

In this section, we describe our approach to rendering forms in Bootstrap 5.

Reference: https://getbootstrap.com/docs/5.0/forms/validation/

Structure of a rendered field
-----------------------------

A rendered fields has these components:

- wrapper
- label (optional)
- field
- help text (optional)
- validation texts (optional)

See below for an example.

.. code:: html

    <div class="mb-3"> <!-- wrapper start -->
        <label for="name" class="form-label">Email address</label> <!-- label -->
        <input type="text" class="form-control" id="name" aria-describedby="nameHelp"> <!-- field -->
        <div id="nameHelp" class="form-text">An alias is fine.</div> <!-- help text -->
        <div class="valid-feedback">Looks good!</div> <!-- validation text -->
    </div>

How and in which order these will components be rendered differs per widget type.

1. We must support `bootstrap_formset`, `bootstrap_form`, and `bootstrap_field` to render a sensible default layout for the above components.
2. We should offer support to easily set or override the classes for the wrapper.
3. We could offert the option to override the templates used to generate this output.

Input groups for more complex fields
------------------------------------

Reference: https://getbootstrap.com/docs/5.0/forms/input-group/

Bootstrap 5 offers Input groups to combine fields and add-ons (both before and after the field).

1. We must support separate rendering of labels, fields, help texts and errors so that users can build their own input groups.
2. We should offer support for add-ons (before and after) as part of `bootstrap_field`.
3. We could add support in form, field or widget definition to define add-ons in Python code.

Note: input-group needs has-validation
https://github.com/twbs/bootstrap/blob/6b3254536bac263c39e3a536c3c13945210d91b2/site/content/docs/5.0/migration.md

Floating labels
---------------

Reference: https://getbootstrap.com/docs/5.0/forms/floating-labels/

This behavior can be triggere dby setting `layout="floating"`.

Floating labels are supported for widgets that can use `form-control`. An exception is `FileInput` and its descendants, those labels cannot be floating.

Setting `layout="floating"` has no effect on widgets that are not supported.