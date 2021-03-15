from django.forms.utils import flatatt
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from django_bootstrap5.text import text_value
from django_bootstrap5.utils import sanitize_url_dict


def render_script_tag(url):
    """Build a script tag."""
    url_dict = sanitize_url_dict(url)
    url_dict.setdefault("src", url_dict.pop("url", None))
    return render_tag("script", url_dict)


def render_link_tag(url, rel="stylesheet", media=None):
    """Build a link tag."""
    url_dict = sanitize_url_dict(url, url_attr="href")
    url_dict.setdefault("href", url_dict.pop("url", None))
    url_dict["rel"] = rel
    if media:
        url_dict["media"] = media
    return render_tag("link", attrs=url_dict, close=False)


def render_tag(tag, attrs=None, content=None, close=True):
    """Render a HTML tag."""
    builder = "<{tag}{attrs}>{content}"
    if content or close:
        builder += "</{tag}>"
    return format_html(builder, tag=tag, attrs=mark_safe(flatatt(attrs)) if attrs else "", content=text_value(content))
