from django.contrib.messages import constants as DEFAULT_MESSAGE_LEVELS

from tests.base import BootstrapTestCase


class MockMessage(object):
    """Follows the `django.contrib.messages.storage.base.Message` API."""

    level = None
    message = None
    extra_tags = None

    def __init__(self, level, message, extra_tags=None):
        self.level = level
        self.extra_tags = extra_tags
        self.message = message

    def __str__(self):
        return self.message


class MessagesTestCase(BootstrapTestCase):
    def _html(self, content, css_class):
        return (
            f'<div class="alert {css_class} alert-dismissible fade show" role="alert">'
            f"{content}"
            '<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>'
            "</div>"
        )

    def test_bootstrap_messages(self):
        messages = [MockMessage(DEFAULT_MESSAGE_LEVELS.WARNING, "hello")]
        self.assertHTMLEqual(
            self.render("{% bootstrap_messages messages %}", {"messages": messages}),
            self._html(content="hello", css_class="alert-warning"),
        )

        messages = [MockMessage(DEFAULT_MESSAGE_LEVELS.ERROR, "hello")]
        self.assertHTMLEqual(
            self.render("{% bootstrap_messages messages %}", {"messages": messages}),
            self._html(content="hello", css_class="alert-danger"),
        )

    def test_bootstrap_messages_with_other_levels(self):
        messages = [MockMessage(None, "hello")]
        self.assertHTMLEqual(
            self.render("{% bootstrap_messages messages %}", {"messages": messages}),
            self._html(content="hello", css_class="alert-info"),
        )
        messages = [MockMessage(999, "hello")]
        self.assertHTMLEqual(
            self.render("{% bootstrap_messages messages %}", {"messages": messages}),
            self._html(content="hello", css_class="alert-info"),
        )

    def test_bootstrap_messages_with_other_content(self):
        messages = [MockMessage(DEFAULT_MESSAGE_LEVELS.ERROR, "hello http://example.com")]
        self.assertHTMLEqual(
            self.render("{% bootstrap_messages messages %}", {"messages": messages}),
            self._html(content="hello http://example.com", css_class="alert-danger"),
        )

        messages = [MockMessage(DEFAULT_MESSAGE_LEVELS.ERROR, "hello\nthere")]
        self.assertHTMLEqual(
            self.render("{% bootstrap_messages messages %}", {"messages": messages}),
            self._html(content="hello there", css_class="alert-danger"),
        )

    def test_bootstrap_messages_with_invalid_message(self):
        messages = [None]
        self.assertHTMLEqual(
            self.render("{% bootstrap_messages messages %}", {"messages": messages}),
            self._html(content="", css_class="alert-info"),
        )
