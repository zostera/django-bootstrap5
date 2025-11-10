from django.core.paginator import Paginator

from django_bootstrap5.utils import url_replace_param
from tests.base import BootstrapTestCase


class PaginatorTestCase(BootstrapTestCase):
    @classmethod
    def setUpTestData(cls):
        cls.beatles = ["john", "paul", "george", "ringo"]
        cls.paginator = Paginator(cls.beatles, 2)

    def test_url_replace_param(self):
        self.assertEqual(url_replace_param("/foo/bar?baz=foo", "baz", "yohoo"), "/foo/bar?baz=yohoo")
        self.assertEqual(url_replace_param("/foo/bar?baz=foo", "baz", None), "/foo/bar")
        self.assertEqual(url_replace_param("/foo/bar#id", "baz", "foo"), "/foo/bar?baz=foo#id")

    def bootstrap_pagination(self, page, extra=""):
        """Render bootstrap_pagination tag."""
        return self.render(f"{{% bootstrap_pagination page {extra} %}}", {"page": page})

    def test_paginator(self):
        html = self.bootstrap_pagination(self.paginator.page(2), extra='url="/projects/?foo=bar"')
        self.assertHTMLEqual(
            html,
            (
                '<ul class="pagination">'
                '<li class="page-item"><a class="page-link" href="/projects/?foo=bar&page=1">&laquo;</a></li>'
                '<li class="page-item"><a class="page-link" href="/projects/?foo=bar&page=1">1</a></li>'
                '<li class="page-item active"><a class="page-link" href="#">2</a></li>'
                '<li class="page-item disabled"><a class="page-link" href="#">&raquo;</a></li>'
                "</ul>"
            ),
        )

        html = self.bootstrap_pagination(self.paginator.page(2), extra='url="/projects/#id"')
        self.assertIn("/projects/?page=1#id", html)
        self.assertNotIn("/projects/?page=2#id", html)

        html = self.bootstrap_pagination(self.paginator.page(2), extra='url="/projects/?page=3#id"')
        self.assertIn("/projects/?page=1#id", html)
        self.assertNotIn("/projects/?page=2#id", html)

        html = self.bootstrap_pagination(self.paginator.page(2), extra='url="/projects/?page=3" extra="id=20"')
        self.assertIn("/projects/?page=1&id=20", html)
        self.assertNotIn("/projects/?page=2&id=20", html)

    def test_paginator_size(self):
        self.assertHTMLEqual(
            self.render('{% bootstrap_pagination page size="sm" %}', {"page": self.paginator.page(2)}),
            (
                '<ul class="pagination pagination-sm">'
                '<li class="page-item"><a class="page-link" href="?page=1">&laquo;</a></li>'
                '<li class="page-item"><a class="page-link" href="?page=1">1</a></li>'
                '<li class="page-item active"><a class="page-link" href="#">2</a></li>'
                '<li class="page-item disabled"><a class="page-link" href="#">&raquo;</a></li>'
                "</ul>"
            ),
        )
        self.assertHTMLEqual(
            self.render('{% bootstrap_pagination page size="lg" %}', {"page": self.paginator.page(2)}),
            (
                '<ul class="pagination pagination-lg">'
                '<li class="page-item"><a class="page-link" href="?page=1">&laquo;</a></li>'
                '<li class="page-item"><a class="page-link" href="?page=1">1</a></li>'
                '<li class="page-item active"><a class="page-link" href="#">2</a></li>'
                '<li class="page-item disabled"><a class="page-link" href="#">&raquo;</a></li>'
                "</ul>"
            ),
        )
        self.assertHTMLEqual(
            self.render('{% bootstrap_pagination page size="md" %}', {"page": self.paginator.page(2)}),
            (
                '<ul class="pagination">'
                '<li class="page-item"><a class="page-link" href="?page=1">&laquo;</a></li>'
                '<li class="page-item"><a class="page-link" href="?page=1">1</a></li>'
                '<li class="page-item active"><a class="page-link" href="#">2</a></li>'
                '<li class="page-item disabled"><a class="page-link" href="#">&raquo;</a></li>'
                "</ul>"
            ),
        )

        with self.assertRaisesRegex(ValueError, 'Invalid value "xl" for parameter'):
            self.render('{% bootstrap_pagination page size="xl" %}', {"page": self.paginator.page(2)})

    def test_paginator_justify(self):
        self.assertHTMLEqual(
            self.render('{% bootstrap_pagination page justify_content="center" %}', {"page": self.paginator.page(2)}),
            (
                '<ul class="pagination justify-content-center">'
                '<li class="page-item"><a class="page-link" href="?page=1">&laquo;</a></li>'
                '<li class="page-item"><a class="page-link" href="?page=1">1</a></li>'
                '<li class="page-item active"><a class="page-link" href="#">2</a></li>'
                '<li class="page-item disabled"><a class="page-link" href="#">&raquo;</a></li>'
                "</ul>"
            ),
        )
        with self.assertRaises(ValueError):
            self.render(
                '{{% bootstrap_pagination page justify_content="somewhere" %}', {"page": self.paginator.page(2)}
            )

    def test_paginator_illegal(self):
        with self.assertRaises(ValueError):
            self.render('{% bootstrap_pagination page pages_to_show="foo" %}', {"page": self.paginator.page(2)})
        with self.assertRaises(ValueError):
            self.render("{{% bootstrap_pagination page pages_to_show=-5 %}", {"page": self.paginator.page(2)})

    def test_paginator_extra_css(self):
        """Test only the extra_classes parameter."""
        # Test with single CSS class
        self.assertHTMLEqual(
                self.render('{% bootstrap_pagination page extra_classes="custom-pagination" %}', {"page": self.paginator.page(2)}),
                (
                    '<ul class="pagination custom-pagination">'
                    '<li class="page-item"><a class="page-link" href="?page=1">&laquo;</a></li>'
                    '<li class="page-item"><a class="page-link" href="?page=1">1</a></li>'
                    '<li class="page-item active"><a class="page-link" href="#">2</a></li>'
                    '<li class="page-item disabled"><a class="page-link" href="#">&raquo;</a></li>'
                    "</ul>"
                    ),
                )

        # Test with multiple CSS classes
        self.assertHTMLEqual(
                self.render('{% bootstrap_pagination page extra_classes="my-custom-class another-class" %}', {"page": self.paginator.page(2)}),
                (
                    '<ul class="pagination my-custom-class another-class">'
                    '<li class="page-item"><a class="page-link" href="?page=1">&laquo;</a></li>'
                    '<li class="page-item"><a class="page-link" href="?page=1">1</a></li>'
                    '<li class="page-item active"><a class="page-link" href="#">2</a></li>'
                    '<li class="page-item disabled"><a class="page-link" href="#">&raquo;</a></li>'
                    "</ul>"
                    ),
                )

        # Test with empty string (should not add anything)
        self.assertHTMLEqual(
                self.render('{% bootstrap_pagination page extra_classes="" %}', {"page": self.paginator.page(2)}),
                (
                    '<ul class="pagination">'
                    '<li class="page-item"><a class="page-link" href="?page=1">&laquo;</a></li>'
                    '<li class="page-item"><a class="page-link" href="?page=1">1</a></li>'
                    '<li class="page-item active"><a class="page-link" href="#">2</a></li>'
                    '<li class="page-item disabled"><a class="page-link" href="#">&raquo;</a></li>'
                    "</ul>"
                    ),
                )

    def test_paginator_extra_classes_with_size(self):
        """Test extra_classes combined with size parameter."""
        self.assertHTMLEqual(
                self.render('{% bootstrap_pagination page size="sm" extra_classes="custom-small" %}', {"page": self.paginator.page(2)}),
                (
                    '<ul class="pagination pagination-sm custom-small">'
                    '<li class="page-item"><a class="page-link" href="?page=1">&laquo;</a></li>'
                    '<li class="page-item"><a class="page-link" href="?page=1">1</a></li>'
                    '<li class="page-item active"><a class="page-link" href="#">2</a></li>'
                    '<li class="page-item disabled"><a class="page-link" href="#">&raquo;</a></li>'
                    "</ul>"
                    ),
                )

        self.assertHTMLEqual(
                self.render('{% bootstrap_pagination page size="lg" extra_classes="large-custom" %}', {"page": self.paginator.page(2)}),
                (
                    '<ul class="pagination pagination-lg large-custom">'
                    '<li class="page-item"><a class="page-link" href="?page=1">&laquo;</a></li>'
                    '<li class="page-item"><a class="page-link" href="?page=1">1</a></li>'
                    '<li class="page-item active"><a class="page-link" href="#">2</a></li>'
                    '<li class="page-item disabled"><a class="page-link" href="#">&raquo;</a></li>'
                    "</ul>"
                    ),
                )

    def test_paginator_extra_classes_with_justify(self):
        """Test extra_classes combined with justify_content parameter."""
        self.assertHTMLEqual(
                self.render('{% bootstrap_pagination page justify_content="center" extra_classes="centered-custom" %}', {"page": self.paginator.page(2)}),
                (
                    '<ul class="pagination justify-content-center centered-custom">'
                    '<li class="page-item"><a class="page-link" href="?page=1">&laquo;</a></li>'
                    '<li class="page-item"><a class="page-link" href="?page=1">1</a></li>'
                    '<li class="page-item active"><a class="page-link" href="#">2</a></li>'
                    '<li class="page-item disabled"><a class="page-link" href="#">&raquo;</a></li>'
                    "</ul>"
                    ),
                )

        self.assertHTMLEqual(
                self.render('{% bootstrap_pagination page justify_content="end" extra_classes="end-aligned" %}', {"page": self.paginator.page(2)}),
                (
                    '<ul class="pagination justify-content-end end-aligned">'
                    '<li class="page-item"><a class="page-link" href="?page=1">&laquo;</a></li>'
                    '<li class="page-item"><a class="page-link" href="?page=1">1</a></li>'
                    '<li class="page-item active"><a class="page-link" href="#">2</a></li>'
                    '<li class="page-item disabled"><a class="page-link" href="#">&raquo;</a></li>'
                    "</ul>"
                    ),
                )

    def test_paginator_extra_classes_with_all_options(self):
        """Test extra_classes combined with size and justify_content parameters."""
        self.assertHTMLEqual(
                self.render('{% bootstrap_pagination page size="lg" justify_content="center" extra_classes="all-options-test" %}', {"page": self.paginator.page(2)}),
                (
                    '<ul class="pagination pagination-lg justify-content-center all-options-test">'
                    '<li class="page-item"><a class="page-link" href="?page=1">&laquo;</a></li>'
                    '<li class="page-item"><a class="page-link" href="?page=1">1</a></li>'
                    '<li class="page-item active"><a class="page-link" href="#">2</a></li>'
                    '<li class="page-item disabled"><a class="page-link" href="#">&raquo;</a></li>'
                    "</ul>"
                    ),
                )

    def test_paginator_extra_classes_with_url_and_extra(self):
        """Test extra_classes with URL and extra parameters."""
        html = self.bootstrap_pagination(
                self.paginator.page(2),
                extra='url="/projects/?foo=bar" extra_classes="url-test-class"'
                )
        self.assertHTMLEqual(
                html,
                (
                    '<ul class="pagination url-test-class">'
                    '<li class="page-item"><a class="page-link" href="/projects/?foo=bar&page=1">&laquo;</a></li>'
                    '<li class="page-item"><a class="page-link" href="/projects/?foo=bar&page=1">1</a></li>'
                    '<li class="page-item active"><a class="page-link" href="#">2</a></li>'
                    '<li class="page-item disabled"><a class="page-link" href="#">&raquo;</a></li>'
                    "</ul>"
                    ),
                )


class LargePaginatorTestCase(BootstrapTestCase):
    @classmethod
    def setUpTestData(cls):
        cls.numbers = [f"{number}" for number in range(1, 100)]
        cls.paginator = Paginator(cls.numbers, 2)

    def test_paginator_ellipsis(self):
        html = self.render("{{% bootstrap_pagination page %}", {"page": self.paginator.page(33)})
        self.assertInHTML('<li class="page-item"><a class="page-link" href="?page=23">&hellip;</a></li>', html)
        self.assertInHTML('<li class="page-item"><a class="page-link" href="?page=43">&hellip;</a></li>', html)

        html = self.render("{{% bootstrap_pagination page %}", {"page": self.paginator.page(2)})
        self.assertInHTML('<li class="page-item"><a class="page-link" href="?page=17">&hellip;</a></li>', html)
        self.assertInHTML("&hellip;", html, count=1)

        html = self.render("{{% bootstrap_pagination page %}", {"page": self.paginator.page(49)})
        self.assertInHTML('<li class="page-item"><a class="page-link" href="?page=38">&hellip;</a></li>', html)
        self.assertInHTML("&hellip;", html, count=1)

    def test_paginator_ellipsis_with_extra_css(self):
        """Test that pagination_extra_classes works correctly with ellipsis pagination."""
        html = self.render('{% bootstrap_pagination page extra_classes="ellipsis-test" %}', {"page": self.paginator.page(33)})

        # Check that the extra CSS class is present
        self.assertIn('class="pagination ellipsis-test"', html)

        # Check that ellipsis are still rendered correctly
        self.assertInHTML('<li class="page-item"><a class="page-link" href="?page=23">&hellip;</a></li>', html)
        self.assertInHTML('<li class="page-item"><a class="page-link" href="?page=43">&hellip;</a></li>', html)
