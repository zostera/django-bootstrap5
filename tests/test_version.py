from django.test import TestCase


class VersionTestCase(TestCase):
    """Test presence of package version."""

    def test_version(self):
        import django_bootstrap5

        version = django_bootstrap5.__version__
        version_parts = version.split(".")
        self.assertTrue(len(version_parts) >= 3)
