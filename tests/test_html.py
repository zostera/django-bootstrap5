from django.test import TestCase
from django.utils.safestring import SafeString, mark_safe

from django_bootstrap5.html import render_multi_line_html, render_tag


class HtmlTestCase(TestCase):
    def test_render_tag(self):
        self.assertEqual(render_tag("span"), "<span></span>")
        self.assertEqual(render_tag("span", content="foo"), "<span>foo</span>")
        self.assertEqual(render_tag("span", attrs={"bar": 123}, content="foo"), '<span bar="123">foo</span>')
        self.assertEqual(render_tag("span", attrs={"bar": "{foo}"}, content="foo"), '<span bar="{foo}">foo</span>')

    def test_render_multi_line_html(self):
        self.assertEqual(render_multi_line_html(), "")
        self.assertEqual(render_multi_line_html([mark_safe("aaa")]), "aaa")

        result = render_multi_line_html([mark_safe("aaa"), mark_safe("bbb")])
        self.assertEqual(result, "aaa\nbbb")
        self.assertTrue(isinstance(result, SafeString))

        result = render_multi_line_html(["<b>aaa</b>", mark_safe("bbb")])
        self.assertEqual(result, "&lt;b&gt;aaa&lt;/b&gt;\nbbb")
        self.assertTrue(isinstance(result, SafeString))
