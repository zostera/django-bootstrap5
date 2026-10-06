"""
Minimal smoke test.

This test verifies that the package can be installed and that
its most basic public API is usable. It intentionally avoids
test frameworks and any optional dependencies.
"""


def main():
    import django

    import django_bootstrap5

    # Basic imports work
    assert django.get_version()
    assert hasattr(django_bootstrap5, "__version__")

    # One minimal functional call
    from django_bootstrap5.css import merge_css_classes

    assert merge_css_classes("btn", "btn btn-primary", "") == "btn btn-primary"


if __name__ == "__main__":
    main()
