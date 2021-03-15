def _css_class_list(list_of_css_classes):
    """Return list without duplicate or empty elements."""
    return filter(None, list(dict.fromkeys(list_of_css_classes)))


def _css_class_list_string(list_of_css_classes):
    """Return string version of list without duplicate or empty elements."""
    return " ".join(_css_class_list(list_of_css_classes))


def merge_css_classes(*args):
    """Merge CSS classes into one string."""
    css_classes = []
    for arg in args:
        css_classes += f"{arg}".split(" ")
    return _css_class_list_string(css_classes)
