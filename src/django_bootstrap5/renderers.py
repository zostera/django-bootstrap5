from bs4 import BeautifulSoup
from django.forms import (
    BaseForm,
    BaseFormSet,
    BoundField,
    CheckboxInput,
    CheckboxSelectMultiple,
    DateInput,
    EmailInput,
    FileInput,
    MultiWidget,
    NumberInput,
    PasswordInput,
    RadioSelect,
    Select,
    SelectDateWidget,
    Textarea,
    TextInput,
    TimeInput,
    URLInput,
)
from django.utils.html import conditional_escape, format_html
from django.utils.safestring import mark_safe

from .core import get_bootstrap_setting
from .css import merge_css_classes
from .exceptions import BootstrapError
from .forms import (
    WRAPPER_CLASS,
    WRAPPER_TAG,
    is_widget_with_placeholder,
    render_field,
    render_form,
    render_form_group,
    render_label,
)
from .text import text_value
from .utils import render_template_file

try:
    # If Django is set up without a database, importing this widget gives RuntimeError
    from django.contrib.auth.forms import ReadOnlyPasswordHashWidget
except RuntimeError:
    ReadOnlyPasswordHashWidget = None


class BaseRenderer(object):
    """A content renderer."""

    SIZES = ["sm", "md", "lg"]

    def __init__(self, *args, **kwargs):
        self.layout = kwargs.get("layout", "")
        self.wrapper_class = kwargs.get("wrapper_class", WRAPPER_CLASS)
        self.field_class = kwargs.get("field_class", "")
        self.label_class = kwargs.get("label_class", "")
        self.show_help = kwargs.get("show_help", True)
        self.show_label = kwargs.get("show_label", True)
        self.exclude = kwargs.get("exclude", "")

        self.set_placeholder = kwargs.get("set_placeholder", True)
        self.size = self.parse_size(kwargs.get("size", ""))
        self.horizontal_label_class = kwargs.get(
            "horizontal_label_class", get_bootstrap_setting("horizontal_label_class")
        )
        self.horizontal_field_class = kwargs.get(
            "horizontal_field_class", get_bootstrap_setting("horizontal_field_class")
        )

    def parse_size(self, size):
        size = text_value(size).lower().strip() or "md"
        if size not in self.SIZES:
            valid_sizes = ", ".join([f'"{size}"' for size in self.SIZES])
            raise BootstrapError(f'Invalid value "{size}" for parameter "size" (valid values are {valid_sizes}).')
        return size

    def get_size_class(self, prefix="form-control"):
        return f"{prefix}-{self.size}" if self.size in ["sm", "lg"] else ""

    def _render(self):
        return ""

    def render(self):
        return mark_safe(self._render())


class FormsetRenderer(BaseRenderer):
    """Default formset renderer."""

    def __init__(self, formset, *args, **kwargs):
        if not isinstance(formset, BaseFormSet):
            raise BootstrapError('Parameter "formset" should contain a valid Django Formset.')
        self.formset = formset
        super().__init__(*args, **kwargs)

    def render_management_form(self):
        return text_value(self.formset.management_form)

    def render_form(self, form, **kwargs):
        return render_form(form, **kwargs)

    def render_forms(self):
        rendered_forms = []
        for form in self.formset.forms:
            rendered_forms.append(
                self.render_form(
                    form,
                    layout=self.layout,
                    form_group_class=self.wrapper_class,
                    field_class=self.field_class,
                    label_class=self.label_class,
                    show_label=self.show_label,
                    show_help=self.show_help,
                    exclude=self.exclude,
                    set_placeholder=self.set_placeholder,
                    size=self.size,
                    horizontal_label_class=self.horizontal_label_class,
                    horizontal_field_class=self.horizontal_field_class,
                )
            )
        return "\n".join(rendered_forms)

    def get_formset_errors(self):
        return self.formset.non_form_errors()

    def render_errors(self):
        formset_errors = self.get_formset_errors()
        if formset_errors:
            return render_template_file(
                "django_bootstrap5/form_errors.html",
                context={"errors": formset_errors, "form": self.formset, "layout": self.layout},
            )
        return ""

    def _render(self):
        return "".join([self.render_errors(), self.render_management_form(), self.render_forms()])


class FormRenderer(BaseRenderer):
    """Default form renderer."""

    def __init__(self, form, *args, **kwargs):
        if not isinstance(form, BaseForm):
            raise BootstrapError('Parameter "form" should contain a valid Django Form.')
        self.form = form
        super().__init__(*args, **kwargs)
        self.error_css_class = kwargs.get("error_css_class", None)
        self.required_css_class = kwargs.get("required_css_class", None)
        self.bound_css_class = kwargs.get("bound_css_class", None)
        self.alert_error_type = kwargs.get("alert_error_type", "non_fields")
        self.form_check_class = kwargs.get("form_check_class", "form-check")

    def render_fields(self):
        rendered_fields = []
        for field in self.form:
            rendered_fields.append(
                render_field(
                    field,
                    layout=self.layout,
                    form_group_class=self.wrapper_class,
                    field_class=self.field_class,
                    label_class=self.label_class,
                    form_check_class=self.form_check_class,
                    show_label=self.show_label,
                    show_help=self.show_help,
                    exclude=self.exclude,
                    set_placeholder=self.set_placeholder,
                    size=self.size,
                    horizontal_label_class=self.horizontal_label_class,
                    horizontal_field_class=self.horizontal_field_class,
                    error_css_class=self.error_css_class,
                    required_css_class=self.required_css_class,
                    bound_css_class=self.bound_css_class,
                )
            )
        return "\n".join(rendered_fields)

    def get_fields_errors(self):
        form_errors = []
        for field in self.form:
            if not field.is_hidden and field.errors:
                form_errors += field.errors
        return form_errors

    def render_errors(self, type="all"):
        form_errors = None
        if type == "all":
            form_errors = self.get_fields_errors() + self.form.non_field_errors()
        elif type == "fields":
            form_errors = self.get_fields_errors()
        elif type == "non_fields":
            form_errors = self.form.non_field_errors()

        if form_errors:
            return render_template_file(
                "django_bootstrap5/form_errors.html",
                context={"errors": form_errors, "form": self.form, "layout": self.layout, "type": type},
            )

        return ""

    def _render(self):
        return self.render_errors(self.alert_error_type) + self.render_fields()


class FieldRenderer(BaseRenderer):
    """Default field renderer."""

    # These widgets will not be wrapped in a form-control class
    WIDGETS_FORM_CONTROL = (TextInput, NumberInput, EmailInput, URLInput, DateInput, TimeInput, Textarea, PasswordInput)
    WIDGETS_NO_FORM_CONTROL = (CheckboxInput, RadioSelect, CheckboxSelectMultiple, FileInput)

    def __init__(self, field, *args, **kwargs):
        if not isinstance(field, BoundField):
            raise BootstrapError('Parameter "field" should contain a valid Django BoundField.')
        self.field = field
        super().__init__(*args, **kwargs)

        self.widget = field.field.widget
        self.is_multi_widget = isinstance(field.field.widget, MultiWidget)
        self.initial_attrs = self.widget.attrs.copy()
        self.help_text = text_value(field.help_text) if self.show_help and field.help_text else ""
        self.field_errors = [conditional_escape(text_value(error)) for error in field.errors]
        self.form_check_class = kwargs.get("form_check_class", "form-check")

        if "placeholder" in kwargs:
            # Find the placeholder in kwargs, even if it's empty
            self.placeholder = kwargs["placeholder"]
        elif get_bootstrap_setting("set_placeholder"):
            # If not found, see if we set the label
            self.placeholder = field.label
        else:
            # Or just set it to empty
            self.placeholder = ""
        if self.placeholder:
            self.placeholder = text_value(self.placeholder)

        self.addon_before = kwargs.get("addon_before", self.widget.attrs.pop("addon_before", ""))
        self.addon_after = kwargs.get("addon_after", self.widget.attrs.pop("addon_after", ""))
        self.addon_before_class = kwargs.get(
            "addon_before_class", self.widget.attrs.pop("addon_before_class", "input-group-text")
        )
        self.addon_after_class = kwargs.get(
            "addon_after_class", self.widget.attrs.pop("addon_after_class", "input-group-text")
        )

        # These are set in Django or in the global BOOTSTRAP5 settings, and can be overwritten in the template
        error_css_class = kwargs.get("error_css_class", None)
        self.error_css_class = (
            getattr(field.form, "error_css_class", get_bootstrap_setting("error_css_class"))
            if error_css_class is None
            else error_css_class
        )

        required_css_class = kwargs.get("required_css_class", None)
        self.required_css_class = (
            getattr(field.form, "required_css_class", get_bootstrap_setting("required_css_class"))
            if required_css_class is None
            else required_css_class
        )
        if self.field.form.empty_permitted:
            self.required_css_class = ""

        bound_css_class = kwargs.get("bound_css_class", None)
        self.success_css_class = (
            getattr(field.form, "bound_css_class", get_bootstrap_setting("success_css_class"))
            if bound_css_class is None
            else bound_css_class
        )

    def restore_widget_attrs(self):
        self.widget.attrs = self.initial_attrs.copy()

    def add_class_attrs(self, widget=None):
        if widget is None:
            widget = self.widget
        size_prefix = None
        classes = widget.attrs.get("class", "")
        if ReadOnlyPasswordHashWidget is not None and isinstance(widget, ReadOnlyPasswordHashWidget):
            # Render this is a static control
            classes = merge_css_classes("form-control-static", classes)
        elif isinstance(widget, self.WIDGETS_FORM_CONTROL):
            classes = merge_css_classes("form-control", classes)
            size_prefix = "form-control"
        elif isinstance(widget, Select):
            classes = merge_css_classes("form-select", classes)
            size_prefix = "form-select"
        elif isinstance(widget, CheckboxInput):
            classes = merge_css_classes("form-check-input", classes)
        elif isinstance(widget, FileInput):
            classes = merge_css_classes("form-control-file", classes)
        if size_prefix:
            classes = merge_css_classes(classes, self.get_size_class(prefix=size_prefix))

        if self.field.errors:
            if self.error_css_class:
                classes = merge_css_classes(classes, self.error_css_class)
        else:
            if self.field.form.is_bound:
                classes = merge_css_classes(classes, self.success_css_class)

        widget.attrs["class"] = classes

    def add_placeholder_attrs(self, widget=None):
        if widget is None:
            widget = self.widget
        placeholder = widget.attrs.get("placeholder", self.placeholder)
        if placeholder and self.set_placeholder and is_widget_with_placeholder(widget):
            # TODO: Should this be stripped and/or escaped?
            widget.attrs["placeholder"] = placeholder

    def add_widget_attrs(self):
        if self.is_multi_widget:
            widgets = self.widget.widgets
        else:
            widgets = [self.widget]
        for widget in widgets:
            self.add_class_attrs(widget)
            self.add_placeholder_attrs(widget)
            if isinstance(widget, (RadioSelect, CheckboxSelectMultiple)):
                widget.template_name = "django_bootstrap5/widgets/radio_select.html"

    def list_to_class(self, html, klass):
        classes = merge_css_classes(klass, self.get_size_class())
        mapping = [
            ("<ul", '<div class="{classes}"'.format(classes=classes)),
            ("</ul>", "</div>"),
            ("<li", '<div class="{form_check_class}"'.format(form_check_class=self.form_check_class)),
            ("</li>", "</div>"),
        ]
        for k, v in mapping:
            html = html.replace(k, v)

        # Apply django_bootstrap5 classes to labels and inputs.
        # A simple 'replace' isn't enough as we don't want to have several 'class' attr definition, which would happen
        # if we tried to 'html.replace("input", "input class=...")'
        soup = BeautifulSoup(html, features="html.parser")
        enclosing_div = soup.find("div", {"class": classes})
        if enclosing_div:
            for label in enclosing_div.find_all("label"):
                label.attrs["class"] = label.attrs.get("class", []) + ["form-check-label"]
                try:
                    label.input.attrs["class"] = label.input.attrs.get("class", []) + ["form-check-input"]
                except AttributeError:
                    pass
        return str(soup)

    def add_checkbox_label(self, html):
        return html + render_label(
            content=self.field.label,
            label_for=self.field.id_for_label,
            label_class="form-check-label",
        )

    def fix_date_select_input(self, html):
        div1 = '<div class="col-4">'
        div2 = "</div>"
        html = html.replace("<select", div1 + "<select")
        html = html.replace("</select>", "</select>" + div2)
        return '<div class="row django_bootstrap5-multi-input">{html}</div>'.format(html=html)

    def fix_file_input_label(self, html):
        html = "<br>" + html
        return html

    def post_widget_render(self, html):
        if isinstance(self.widget, RadioSelect):
            html = self.list_to_class(html, "radio radio-success")
        elif isinstance(self.widget, CheckboxSelectMultiple):
            html = self.list_to_class(html, "checkbox")
        elif isinstance(self.widget, SelectDateWidget):
            html = self.fix_date_select_input(html)
        elif isinstance(self.widget, CheckboxInput):
            html = self.add_checkbox_label(html)
        elif isinstance(self.widget, FileInput):
            html = self.fix_file_input_label(html)
        return html

    def wrap_widget(self, html):
        if isinstance(self.widget, CheckboxInput):
            # Wrap checkboxes
            # Note checkboxes do not get size classes, see #318
            html = '<div class="form-check">{html}</div>'.format(html=html)
        return html

    def make_input_group_addon(self, inner_class, outer_class, content):
        if not content:
            return ""
        if inner_class:
            content = '<span class="{inner_class}">{content}</span>'.format(inner_class=inner_class, content=content)
        return '<div class="{outer_class}">{content}</div>'.format(outer_class=outer_class, content=content)

    @property
    def is_input_group(self):
        allowed_widget_types = (TextInput, PasswordInput, DateInput, NumberInput, Select, EmailInput)
        return (self.addon_before or self.addon_after) and isinstance(self.widget, allowed_widget_types)

    def make_input_group(self, html):
        if self.is_input_group:
            before = self.make_input_group_addon(self.addon_before_class, "input-group-prepend", self.addon_before)
            after = self.make_input_group_addon(self.addon_after_class, "input-group-append", self.addon_after)
            html = self.append_errors("{before}{html}{after}".format(before=before, html=html, after=after))
            html = '<div class="input-group">{html}</div>'.format(html=html)
        return html

    def append_errors(self, html):
        field_errors = self.field_errors
        if field_errors:
            errors_html = render_template_file(
                "django_bootstrap5/field_errors.html",
                context={
                    "field": self.field,
                    "field_errors": field_errors,
                    "layout": self.layout,
                    "show_help": self.show_help,
                },
            )
            html += errors_html
        return html

    def append_to_field(self, html):
        if isinstance(self.widget, CheckboxInput):
            # we have already appended errors and help to checkboxes
            # in append_to_checkbox_field
            return html

        if not self.is_input_group:
            # we already appended errors for input groups in make_input_group
            html = self.append_errors(html)

        return self.append_help(html)

    def append_to_checkbox_field(self, html):
        if not isinstance(self.widget, CheckboxInput):
            # we will append errors and help to normal fields later in append_to_field
            return html

        html = self.append_errors(html)
        return self.append_help(html)

    def get_field_class(self):
        field_class = self.field_class
        if not field_class and self.layout == "horizontal":
            field_class = self.horizontal_field_class
        return field_class

    def wrap_field(self, html):
        field_class = self.get_field_class()
        if field_class:
            html = '<div class="{field_class}">{html}</div>'.format(field_class=field_class, html=html)
        return html

    def get_label_class(self):
        label_classes = [text_value(self.label_class)]
        if not self.show_label:
            label_classes.append("visually-hidden")
        else:
            if isinstance(self.widget, CheckboxInput):
                widget_label_class = "form-check-label"
            else:
                widget_label_class = "form-label"
            label_classes = [widget_label_class] + label_classes
        return merge_css_classes(*label_classes)

    def get_label_html(self):
        """Return value for label."""
        label_html = "" if self.show_label == "skip" else self.field.label
        if label_html:
            label_html = render_label(label_html, label_for=self.field.id_for_label, label_class=self.get_label_class())
        return label_html

    def wrap_label_and_field(self, html):
        return render_form_group(html, self.get_form_group_class())

    def get_field_html(self):
        """Return HTML for field."""
        self.add_widget_attrs()
        field_html = self.field.as_widget(attrs=self.widget.attrs)
        self.restore_widget_attrs()
        return field_html

    def get_help_html(self):
        """Return HTML for help text, or empty string if there is none."""
        help_text = self.help_text or ""
        if help_text:
            return render_template_file(
                "django_bootstrap5/field_help_text.html",
                context={
                    "field": self.field,
                    "help_text": help_text,
                    "layout": self.layout,
                    "show_help": self.show_help,
                },
            )
        return ""

    def get_errors_html(self):
        field_errors = self.field_errors
        if field_errors:
            return render_template_file(
                "django_bootstrap5/field_errors.html",
                context={
                    "field": self.field,
                    "field_errors": field_errors,
                    "layout": self.layout,
                    "show_help": self.show_help,
                },
            )
        return ""

    def get_wrapper_classes(self):
        wrapper_classes = [self.wrapper_class]
        if self.field.errors:
            wrapper_classes.append(self.error_css_class)
        elif self.field.form.is_bound:
            wrapper_classes.append(self.success_css_class)
        if self.field.field.required:
            wrapper_classes.append(self.required_css_class)
        wrapper_classes.append("mb-3")
        return merge_css_classes(*wrapper_classes)

    def field_before_label(self):
        return isinstance(self.widget, (CheckboxInput,))

    def _render(self):
        if self.field.name in self.exclude.replace(" ", "").split(","):
            return ""
        if self.field.is_hidden:
            return text_value(self.field)

        field = self.get_field_html()

        label = self.get_label_html()

        field_with_label = field + label if self.field_before_label() else label + field

        if isinstance(self.widget, CheckboxInput):
            field_with_label = format_html('<div class="form-check">{}</div>', field_with_label)

        return format_html(
            '<{tag} class="{wrapper_classes}">{field_with_label}{help}{errors}</{tag}>',
            tag=WRAPPER_TAG,
            wrapper_classes=self.get_wrapper_classes(),
            field_with_label=field_with_label,
            help=self.get_help_html(),
            errors=self.get_errors_html(),
        )
