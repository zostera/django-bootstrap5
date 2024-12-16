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

        self.assertHTMLEqual(
            self.render("{% bootstrap_button 'button' formaction='/somewhere/else' %}"),
            '<button class="btn btn-primary" formaction="/somewhere/else">button</button>',
        )

    def test_button_classes(self):
        self.assertHTMLEqual(
            self.render("{% bootstrap_button 'button' button_class='btn-outline-primary' %}"),
            '<button class="btn btn-outline-primary">button</button>',
        )

    def test_button_content(self):
        self.assertHTMLEqual(
            self.render("{% bootstrap_button '<i>button</i>' %}"),
            '<button class="btn btn-primary"><i>button</i></button>',
        )
        self.assertHTMLEqual(
            self.render("{% bootstrap_button content %}", {"content": "<i>button</i>"}),
            '<button class="btn btn-primary">&lt;i&gt;button&lt;/i&gt;</button>',
        )
        self.assertHTMLEqual(
            self.render("{% bootstrap_button content|safe %}", {"content": "<i>button</i>"}),
            '<button class="btn btn-primary"><i>button</i></button>',
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

        with self.assertRaises(ValueError):
            self.render("{% bootstrap_button 'button' button_type='button' href='#' %}")

    def test_button_hyphenate_attributes(self):
        # No attributes to hyphenate
        self.assertHTMLEqual(
            self.render("{% bootstrap_button 'button' href='#' %}"),
            '<a class="btn btn-primary" href="#" role="button">button</a>',
        )

        # Default prefix: data
        self.assertHTMLEqual(
            self.render("{% bootstrap_button 'button' href='#' data_foo='bar' %}"),
            '<a class="btn btn-primary" href="#" role="button" data-foo="bar">button</a>',
        )

        # Default prefix: no hx
        self.assertHTMLEqual(
            self.render("{% bootstrap_button 'button' href='#' data_foo='bar' hx_xyz='abc' %}"),
            '<a class="btn btn-primary" href="#" role="button" data-foo="bar" hx_xyz="abc">button</a>',
        )

        # Custom prefix: data and hx
        with self.settings(BOOTSTRAP5={"hyphenate_attribute_prefixes": ["data", "hx"]}):
            self.assertHTMLEqual(
                self.render("{% bootstrap_button 'button' href='#' data_foo='bar' hx_xyz='abc' %}"),
                '<a class="btn btn-primary" href="#" role="button" data-foo="bar" hx-xyz="abc">button</a>',
            )

        # Custom prefix: hx only
        with self.settings(BOOTSTRAP5={"hyphenate_attribute_prefixes": ["hx"]}):
            self.assertHTMLEqual(
                self.render("{% bootstrap_button 'button' href='#' data_foo='bar' hx_xyz='abc' %}"),
                '<a class="btn btn-primary" href="#" role="button" data_foo="bar" hx-xyz="abc">button</a>',
            )

        # Custom prefix: empty list
        with self.settings(BOOTSTRAP5={"hyphenate_attribute_prefixes": []}):
            self.assertHTMLEqual(
                self.render("{% bootstrap_button 'button' href='#' data_foo='bar' hx_xyz='abc' %}"),
                '<a class="btn btn-primary" href="#" role="button" data_foo="bar" hx_xyz="abc">button</a>',
            )

        # Custom prefix: None
        with self.settings(BOOTSTRAP5={"hyphenate_attribute_prefixes": None}):
            self.assertHTMLEqual(
                self.render("{% bootstrap_button 'button' href='#' data_foo='bar' hx_xyz='abc' %}"),
                '<a class="btn btn-primary" href="#" role="button" data_foo="bar" hx_xyz="abc">button</a>',
            )

        # Edge case: attribute name starts with prefix but prefix is not followed by underscore
        self.assertHTMLEqual(
            self.render("{% bootstrap_button 'button' href='#' databar_foo='bar' %}"),
            '<a class="btn btn-primary" href="#" role="button" databar_foo="bar">button</a>',
        )
