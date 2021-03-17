from django.test import TestCase

from django_bootstrap5.css import merge_css_classes


class CssTest(TestCase):
    def test_merge_css_classes(self):
        css_classes = "one two"
        css_class = "three four"
        classes = merge_css_classes(css_classes, css_class)
        self.assertEqual(classes, "one two three four")

        classes = merge_css_classes(css_class, css_classes)
        self.assertEqual(classes, "three four one two")
