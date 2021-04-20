from django.core.paginator import Paginator

from django_bootstrap5.utils import url_replace_param
from tests.base import BootstrapTestCase


class PaginatorTestCase(BootstrapTestCase):
    def test_url_replace_param(self):
        self.assertEqual(url_replace_param("/foo/bar?baz=foo", "baz", "yohoo"), "/foo/bar?baz=yohoo")
        self.assertEqual(url_replace_param("/foo/bar?baz=foo", "baz", None), "/foo/bar")
        self.assertEqual(url_replace_param("/foo/bar#id", "baz", "foo"), "/foo/bar?baz=foo#id")

    def bootstrap_pagination(self, page, extra=""):
        """Helper to test bootstrap_pagination tag."""
        return self.render(f"{{% bootstrap_pagination page {extra} %}}", {"page": page})

    def test_paginator(self):
        objects = ["john", "paul", "george", "ringo"]
        paginator = Paginator(objects, 2)

        html = self.bootstrap_pagination(paginator.page(2), extra='url="/projects/?foo=bar"')
        self.assertHTMLEqual(
            html,
            """
<nav>
    <ul class="pagination">
        <li class="page-item"><a class="page-link" href="/projects/?foo=bar&page=1">&laquo;</a></li>
        <li class="page-item"><a class="page-link" href="/projects/?foo=bar&page=1">1</a></li>
        <li class="page-item active"><a class="page-link" href="#">2</a></li>
        <li class="page-item disabled"><a class="page-link" href="#">&raquo;</a></li>
    </ul>
</nav>
    """,
        )
        self.assertIn("/projects/?foo=bar&page=1", html)
        self.assertNotIn("/projects/?foo=bar&page=2", html)

        html = self.bootstrap_pagination(paginator.page(2), extra='url="/projects/#id"')
        self.assertIn("/projects/?page=1#id", html)
        self.assertNotIn("/projects/?page=2#id", html)

        html = self.bootstrap_pagination(paginator.page(2), extra='url="/projects/?page=3#id"')
        self.assertIn("/projects/?page=1#id", html)
        self.assertNotIn("/projects/?page=2#id", html)

        html = self.bootstrap_pagination(paginator.page(2), extra='url="/projects/?page=3" extra="id=20"')
        self.assertIn("/projects/?page=1&id=20", html)
        self.assertNotIn("/projects/?page=2&id=20", html)
