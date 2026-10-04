import json
import tempfile
from pathlib import Path

from django.templatetags.static import static
from django.utils.functional import lazy

from django_bootstrap5.core import get_bootstrap_setting
from tests.base import BootstrapTestCase

lazy_static = lazy(static, str)


class MediaTestCase(BootstrapTestCase):
    expected_bootstrap_css = (
        '<link href="{url}" integrity="{integrity}" crossorigin="{crossorigin}" rel="stylesheet">'.format(
            **get_bootstrap_setting("css_url")
        )
    )
    expected_bootstrap_js = '<script src="{url}" integrity="{integrity}" crossorigin="{crossorigin}"></script>'.format(
        **get_bootstrap_setting("javascript_url")
    )

    def test_bootstrap_javascript_tag(self):
        self.assertHTMLEqual(
            self.render("{% bootstrap_javascript %}"),
            self.expected_bootstrap_js,
        )
        with self.settings(BOOTSTRAP5={"javascript_url": "//example.com/bootstrap.js"}):
            self.assertHTMLEqual(
                self.render("{% bootstrap_javascript %}"),
                '<script src="//example.com/bootstrap.js">',
            )

    def test_bootstrap_css_tag(self):
        self.assertHTMLEqual(
            self.render("{% bootstrap_css %}"),
            self.expected_bootstrap_css,
        )
        with self.settings(BOOTSTRAP5={"css_url": "//example.com/bootstrap.css"}):
            self.assertHTMLEqual(
                self.render("{% bootstrap_css %}"),
                '<link href="//example.com/bootstrap.css" rel="stylesheet">',
            )

    def test_bootstrap_css_tag_with_theme(self):
        with self.settings(BOOTSTRAP5={"theme_url": "//example.com/theme.css"}):
            self.assertHTMLEqual(
                self.render("{% bootstrap_css %}"),
                self.expected_bootstrap_css + '<link rel="stylesheet" href="//example.com/theme.css">',
            )

    def test_bootstrap_setting_tag(self):
        self.assertEqual(
            self.render('{% bootstrap_setting "required_css_class" %}'),
            "django_bootstrap5-req",
        )
        self.assertEqual(
            self.render(
                '{% bootstrap_setting "javascript_in_head" as BOOTSTRAP_JAVASCRIPT_IN_HEAD %}'
                + "{% if BOOTSTRAP_JAVASCRIPT_IN_HEAD %}head{% else %}body{% endif %}"
            ),
            "head",
        )


class StaticUrlTestCase(BootstrapTestCase):
    """Test serving Bootstrap from the staticfiles app, with hashed filenames."""

    hashed_name = "css/bootstrap.min.0123456789ab.css"

    def manifest_settings(self, static_root, **bootstrap5):
        """Return settings using ManifestStaticFilesStorage with a manifest for the CSS file."""
        Path(static_root, "staticfiles.json").write_text(
            json.dumps({"version": "1.1", "hash": "", "paths": {"css/bootstrap.min.css": self.hashed_name}})
        )
        return self.settings(
            STATIC_ROOT=static_root,
            STORAGES={
                "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
                "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.ManifestStaticFilesStorage"},
            },
            BOOTSTRAP5=bootstrap5,
        )

    def test_lazy_static_css_url(self):
        """A lazy static url as css_url is resolved by the storage at render time."""
        with tempfile.TemporaryDirectory() as static_root:
            with self.manifest_settings(static_root, css_url=lazy_static("css/bootstrap.min.css")):
                self.assertHTMLEqual(
                    self.render("{% bootstrap_css %}"),
                    f'<link href="/static/{self.hashed_name}" rel="stylesheet">',
                )

    def test_lazy_static_css_url_in_dict(self):
        """A lazy static url in the dict form of css_url is resolved, keeping the other attributes."""
        with tempfile.TemporaryDirectory() as static_root:
            with self.manifest_settings(
                static_root,
                css_url={"url": lazy_static("css/bootstrap.min.css"), "crossorigin": "anonymous"},
            ):
                self.assertHTMLEqual(
                    self.render("{% bootstrap_css %}"),
                    f'<link href="/static/{self.hashed_name}" crossorigin="anonymous" rel="stylesheet">',
                )
