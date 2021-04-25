from django_bootstrap5.exceptions import BootstrapError
from tests.base import BootstrapTestCase


class ButtonTestCase(BootstrapTestCase):
    def test_button(self):
        self.assertHTMLEqual(
            self.render("{% bootstrap_button 'button' size='lg' %}"),
            '<button class="btn btn-primary btn-lg">button</button>',
        )

        self.assertHTMLEqual(
            self.render("{% bootstrap_button 'button' id='foo' %}"),
            '<button class="btn btn-primary" id="foo">button</button>',
        )

        self.assertHTMLEqual(
            self.render("{% bootstrap_button 'button' name='foo' %}"),
            '<button class="btn btn-primary" name="foo">button</button>',
        )

        self.assertHTMLEqual(
            self.render("{% bootstrap_button 'button' value='foo' %}"),
            '<button class="btn btn-primary" value="foo">button</button>',
        )

        self.assertHTMLEqual(
            self.render("{% bootstrap_button 'button' title='foo' %}"),
            '<button class="btn btn-primary" title="foo">button</button>',
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
