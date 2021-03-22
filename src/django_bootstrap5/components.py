from django.template.defaultfilters import capfirst
from django.utils.html import format_html
from django.utils.translation import gettext as _

from .css import merge_css_classes
from .html import render_tag

ALERT_TYPES = ["primary", "secondary", "success", "danger", "warning", "info", "light", "dark"]


def render_alert(content, alert_type="info", dismissible=True, extra_classes=""):
    """Render a Bootstrap alert."""
    button = ""
    if alert_type not in ALERT_TYPES:
        raise ValueError(f"Value {alert_type} is not a valid alert type. Please choose from {', '.join(ALERT_TYPES)}.")
    css_classes = [f"alert alert-{alert_type}"]
    if dismissible:
        css_classes.append("alert-dismissible fade show")
        close = capfirst(_("close"))
        button = f'<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="{close}"></button>'
    css_classes = merge_css_classes(*css_classes)
    return render_tag(
        "div",
        attrs={"class": css_classes, "role": "alert"},
        content=format_html("{content}" + button, content=content),
    )
