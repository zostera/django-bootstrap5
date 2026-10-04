from django.test import TestCase

from django_bootstrap5.text import text_value


class TextTestCase(TestCase):
    def test_text_value(self):
        self.assertEqual(text_value(""), "")
        self.assertEqual(text_value(" "), " ")
        self.assertEqual(text_value(None), "")
        self.assertEqual(text_value(1), "1")
