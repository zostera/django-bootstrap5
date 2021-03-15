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