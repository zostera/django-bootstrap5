from django import get_version
from django.template import engines
from django.test import TestCase

DJANGO_VERSION = get_version()


class BootstrapTestCase(TestCase):
    """TestCase with render function for template code."""

    def render(self, text, context=None, load_bootstrap=True):
        """Return rendered result of template with given context."""
        prefix = "{% load django_bootstrap5 %}" if load_bootstrap else ""
        template = engines["django"].from_string(f"{prefix}{text}")
        return template.render(context or {})
