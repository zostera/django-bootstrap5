from django_bootstrap5.exceptions import BootstrapError
from tests.base import BootstrapTestCase


class BootstrapFormSetTestCase(BootstrapTestCase):
    def test_illegal_formset(self):
        with self.assertRaises(BootstrapError):
            self.render("{% bootstrap_formset formset %}", {"formset": "illegal"})
