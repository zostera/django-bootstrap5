from django.utils.encoding import force_str


def text_value(value):
    """Force a value to text, render None as an empty string."""
    if value is None:
        return ""
    return force_str(value)
