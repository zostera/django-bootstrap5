from django.utils.safestring import mark_safe

from .core import get_field_renderer, get_form_renderer, get_formset_renderer
from .css import merge_css_classes
from .exceptions import BootstrapError
from .html import render_tag
from .size import DEFAULT_SIZE, SIZE_MD, get_size_class

WRAPPER_CLASS = ""
WRAPPER_TAG = "div"


def render_formset(formset, **kwargs):
    """Render a formset to a Bootstrap layout."""
    renderer_cls = get_formset_renderer(**kwargs)
    return renderer_cls(formset, **kwargs).render()


def render_formset_errors(formset, **kwargs):
    """Render formset errors to a Bootstrap layout."""
    renderer_cls = get_formset_renderer(**kwargs)
    return renderer_cls(formset, **kwargs).render_errors()


def render_form(form, **kwargs):
    """Render a form to a Bootstrap layout."""
    renderer_cls = get_form_renderer(**kwargs)
    return renderer_cls(form, **kwargs).render()


def render_form_errors(form, type="all", **kwargs):
    """Render form errors to a Bootstrap layout."""
    renderer_cls = get_form_renderer(**kwargs)
    return renderer_cls(form, **kwargs).render_errors(type)


def render_field(field, **kwargs):
    """Render a field to a Bootstrap layout."""
    renderer_cls = get_field_renderer(**kwargs)
    return renderer_cls(field, **kwargs).render()


def render_label(content, label_for=None, label_class=None, label_title=""):
    """Render a label with content."""
    attrs = {}
    if label_for:
        attrs["for"] = label_for
    if label_class:
        attrs["class"] = label_class
    if label_title:
        attrs["title"] = label_title
    return render_tag("label", attrs=attrs, content=content)


def render_button(
    content,
    button_type=None,
    button_class="btn-primary",
    button_outline=False,
    size="",
    href="",
    name=None,
    value=None,
    title=None,
    extra_classes="",
    id="",
):
    """Render a button with content."""
    attrs = {}
    size_class = get_size_class(size, prefix="btn", skip=SIZE_MD, default=DEFAULT_SIZE)
    classes = merge_css_classes("btn", button_class, size_class)

    if button_type:
        if button_type not in ("submit", "reset", "button", "link"):
            raise BootstrapError(
                (
                    'Parameter "button_type" should be "submit", "reset", "button", "link" or empty '
                    '("{button_type}" given).'
                ).format(button_type=button_type)
            )
        if button_type != "link":
            attrs["type"] = button_type

    classes = merge_css_classes(classes, extra_classes)
    attrs["class"] = classes

    if href:
        tag = "a"
        if button_type and button_type != "link":
            raise BootstrapError(
                'Button of type "{button_type}" is not allowed a "href" parameter.'.format(button_type=button_type)
            )
        attrs["href"] = href
        # Specify role for link with button appearance
        attrs.setdefault("role", "button")
    else:
        tag = "button"

    if id:
        attrs["id"] = id
    if name:
        attrs["name"] = name
    if value:
        attrs["value"] = value
    if title:
        attrs["title"] = title
    return render_tag(tag, attrs=attrs, content=mark_safe(content))
