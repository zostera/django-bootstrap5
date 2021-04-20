from django_bootstrap5.exceptions import BootstrapError
from tests.base import BootstrapTestCase


class ButtonTestCase(BootstrapTestCase):
    def test_button(self):
        self.assertHTMLEqual(
            self.render("{% bootstrap_button 'button' size='lg' %}"),
            '<button class="btn btn-primary btn-lg">button</button>',
        )

    def test_button_type_link(self):
        link_button = '<a class="btn btn-primary btn-lg" href="#" role="button">button</a>'
        self.assertHTMLEqual(
            self.render("{% bootstrap_button 'button' size='lg' href='#' %}"),
            link_button,
        )
        self.assertHTMLEqual(
            self.render("{% bootstrap_button 'button' button_type='link' size='lg' href='#' %}"),
            link_button,
        )

        with self.assertRaises(BootstrapError):
            self.render("{% bootstrap_button 'button' button_type='button' href='#' %}")
