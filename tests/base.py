import functools
from typing import ClassVar, Literal

import jinja2
import jinja2.ext
from django import get_version
from django.template import engines
from django.test import TestCase

DJANGO_VERSION = get_version()


class BootstrapTestCase(TestCase):
    """TestCase with render function for template code."""

    template_engine: ClassVar[Literal["django", "jinja2"]] = "django"

    @functools.cached_property
    def _jinja2_env(self) -> jinja2.Environment:
        """Lazy initialization of jinja2 Environment."""
        from django_bootstrap5.jinja2 import BootstrapTags

        return jinja2.Environment(
            autoescape=True,
            extensions=[jinja2.ext.i18n, BootstrapTags],
            loader=jinja2.FileSystemLoader("tests/templates"),
        )

    def _render_django(self, text, context=None, load_bootstrap=True):
        """Return rendered result of template with given context."""
        prefix = "{% load django_bootstrap5 %}" if load_bootstrap else ""
        template = engines["django"].from_string(f"{prefix}{text}")
        return template.render(context or {})

    def _render_jinja2(self, content: str, /, context=None) -> str:
        """Render the jinja2 html content to string with given context."""
        template = self._jinja2_env.from_string(content)
        return template.render(context or {})

    def render(self, content: str, /, context=None, *args, **kwargs) -> str:
        engine = self.template_engine
        if engine == "django":
            return self._render_django(content, context, *args, **kwargs)
        elif engine == "jinja2":
            return self._render_jinja2(content, context, *args, **kwargs)
