from django.contrib.messages import constants as DEFAULT_MESSAGE_LEVELS

from tests.base import BootstrapTestCase


class FakeMessage(object):
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
    def test_bootstrap_messages(self):
        messages = [FakeMessage(DEFAULT_MESSAGE_LEVELS.WARNING, "hello")]
        html = self.render("{% bootstrap_messages messages %}", {"messages": messages})
        expected = (
            '<div class="alert alert-warning alert-dismissible fade show" role="alert">'
            "hello"
            '<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>'
            "</div>"
        )
        self.assertHTMLEqual(html, expected)

        messages = [FakeMessage(DEFAULT_MESSAGE_LEVELS.ERROR, "hello")]
        html = self.render("{% bootstrap_messages messages %}", {"messages": messages})
        expected = (
            '<div class="alert alert-danger alert-dismissible fade show" role="alert">'
            "hello"
            '<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>'
            "</div>"
        )
        self.assertHTMLEqual(html, expected)

        messages = [FakeMessage(None, "hello")]
        html = self.render("{% bootstrap_messages messages %}", {"messages": messages})
        expected = (
            '<div class="alert alert-info alert-dismissible fade show" role="alert">'
            "hello"
            '<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>'
            "</div>"
        )
        self.assertHTMLEqual(html, expected)

        messages = [FakeMessage(DEFAULT_MESSAGE_LEVELS.ERROR, "hello http://example.com")]
        html = self.render("{% bootstrap_messages messages %}", {"messages": messages})
        expected = (
            '<div class="alert alert-danger alert-dismissible fade show" role="alert">'
            "hello http://example.com"
            '<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>'
            "</div>"
        )
        self.assertHTMLEqual(html, expected)

        messages = [FakeMessage(DEFAULT_MESSAGE_LEVELS.ERROR, "hello\nthere")]
        html = self.render("{% bootstrap_messages messages %}", {"messages": messages})
        expected = (
            '<div class="alert alert-danger alert-dismissible fade show" role="alert">'
            "hello there"
            '<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>'
            "</div>"
        )
        self.assertHTMLEqual(html, expected)
