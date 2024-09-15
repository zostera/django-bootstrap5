from tests.base import BootstrapTestCase
from tests.test_bootstrap_css_and_js_tags import MediaTestCase
from tests.test_bootstrap_field_input_text import CharFieldTestForm
from tests.test_bootstrap_formset import TestFormSet


class Jinja2TestCase(BootstrapTestCase):
    template_engine = "jinja2"

    def test_empty_template(self) -> None:
        self.assertEqual(self.render("").strip(), "")

    def test_text_template(self):
        self.assertEqual(self.render("some text").strip(), "some text")

    def test_alert(self):
        self.assertEqual(
            self.render('{{ bootstrap_alert("content", dismissible=False) }}'),
            '<div class="alert alert-info" role="alert">content</div>',
        )

    def test_button(self):
        self.assertHTMLEqual(
            self.render("{{ bootstrap_button('button', id='foo') }}"),
            '<button class="btn btn-primary" id="foo">button</button>',
        )

    def test_css(self):
        self.assertHTMLEqual(
            self.render("{{ bootstrap_css() }}"),
            MediaTestCase.expected_bootstrap_css,
        )

    def test_js(self):
        self.assertHTMLEqual(
            self.render("{{ bootstrap_javascript() }}"),
            MediaTestCase.expected_bootstrap_js,
        )

    def test_field(self):
        form = CharFieldTestForm()
        self.assertTrue(
            self.render("{{ bootstrap_field(form.test) }}", context={"form": form}),
        )

    def test_form(self):
        form = CharFieldTestForm()
        self.assertTrue(
            self.render("{{ bootstrap_form(form) }}", context={"form": form}),
        )

    def test_formset(self):
        formset = TestFormSet()
        self.assertTrue(
            self.render("{{ bootstrap_formset(formset) }}", context={"formset": formset}),
        )

    def test_label(self):
        self.assertHTMLEqual(
            self.render('{{ bootstrap_label("Subject") }}'),
            '<label class="form-label">Subject</label>',
        )

    def test_pagination(self):
        from django.core.paginator import Paginator

        paginator = Paginator(["john", "paul", "george", "ringo"], 2)
        html = self.render(
            "{{ bootstrap_pagination(page, extra='url=\"/projects/?foo=bar\"') }}}", {"page": paginator.page(1)}
        )
        self.assertTrue(html)

    def test_messages(self):
        from django.contrib.messages import constants as DEFAULT_MESSAGE_LEVELS
        from django.contrib.messages.storage.base import Message

        messages = [Message(DEFAULT_MESSAGE_LEVELS.ERROR, "hello")]
        self.assertTrue(
            self.render("{{ bootstrap_messages() }}", {"messages": messages}),
        )

    def test_setting(self):
        self.assertEqual(
            self.render('{{ bootstrap_setting("required_css_class") }}'),
            "django_bootstrap5-req",
        )
