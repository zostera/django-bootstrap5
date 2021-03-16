import re
from urllib.parse import parse_qs, urlparse, urlunparse

from django.template.base import FilterExpression, TemplateSyntaxError, Variable, VariableDoesNotExist, kwarg_re
from django.template.loader import get_template
from django.utils.encoding import force_str
from django.utils.http import urlencode
from django.utils.safestring import mark_safe

# RegEx for quoted string
QUOTED_STRING = re.compile(r'^["\'](?P<noquotes>.+)["\']$')


def handle_var(value, context):
    """Handle template tag variable."""
    # Resolve FilterExpression and Variable immediately
    if isinstance(value, FilterExpression) or isinstance(value, Variable):
        return value.resolve(context)
    # Return quoted strings unquoted
    # http://djangosnippets.org/snippets/886
    stringval = QUOTED_STRING.search(value)
    if stringval:
        return stringval.group("noquotes")
    # Resolve variable or return string value
    try:
        return Variable(value).resolve(context)
    except VariableDoesNotExist:
        return value


def parse_token_contents(parser, token):
    """Parse template tag contents."""
    bits = token.split_contents()
    tag = bits.pop(0)
    args = []
    kwargs = {}
    asvar = None
    if len(bits) >= 2 and bits[-2] == "as":
        asvar = bits[-1]
        bits = bits[:-2]
    if len(bits):
        for bit in bits:
            match = kwarg_re.match(bit)
            if not match:
                raise TemplateSyntaxError('Malformed arguments to tag "{tag}"'.format(tag=tag))
            name, value = match.groups()
            if name:
                kwargs[name] = parser.compile_filter(value)
            else:
                args.append(parser.compile_filter(value))
    return {"tag": tag, "args": args, "kwargs": kwargs, "asvar": asvar}


def render_template_file(template, context=None):
    """Return rendered template file, with given context as input."""
    template = get_template(template)
    return template.render(context)


def url_replace_param(url, name, value):
    """Replace a GET parameter in an URL."""
    url_components = urlparse(force_str(url))

    params = parse_qs(url_components.query)

    if value is None:
        del params[name]
    else:
        params[name] = value

    return mark_safe(
        urlunparse(
            [
                url_components.scheme,
                url_components.netloc,
                url_components.path,
                url_components.params,
                urlencode(params, doseq=True),
                url_components.fragment,
            ]
        )
    )


def get_url_attrs(url, attr_name):
    """
    Return dictionary with attributes for HTML tag, where the key for url.

    Parameter `url` is either a string or a dict of attrs with the key `url`.
    Parameter `attr_key` is the name for the url value in the results.
    """
    url_attrs = {}
    if isinstance(url, str):
        url = {"url": url}
    url_attrs.update(url)
    url_attrs[attr_name] = url_attrs.pop("url")
    return url_attrs
