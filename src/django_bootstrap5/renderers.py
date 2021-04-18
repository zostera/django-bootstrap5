from django.forms import (
    BaseForm,
    BaseFormSet,
    BoundField,
    CheckboxInput,
    CheckboxSelectMultiple,
    ClearableFileInput,
    MultiWidget,
    RadioSelect,
    Select,
)
from django.forms.widgets import FileInput, Input, Textarea
from django.utils.html import conditional_escape, format_html, strip_tags
from django.utils.safestring import mark_safe

from .core import get_bootstrap_setting
from .css import merge_css_classes
from .exceptions import BootstrapError
from .forms import WRAPPER_CLASS, WRAPPER_TAG, render_field, render_form, render_label
from .size import DEFAULT_SIZE, SIZE_MD, SIZE_XS, get_size_class, parse_size
from .text import text_value
from .utils import render_template_file
from .widgets import ReadOnlyPasswordHashWidget, is_widget_with_placeholder


class BaseRenderer(object):
    """A content renderer."""

    def __init__(self, *args, **kwargs):
        self.layout = kwargs.get("layout", "")
        self.wrapper_class = kwargs.get("wrapper_class", WRAPPER_CLASS)
        self.field_class = kwargs.get("field_class", "")
        self.label_class = kwargs.get("label_class", "")
        self.show_help = kwargs.get("show_help", True)
        self.show_label = kwargs.get("show_label", True)
        self.exclude = kwargs.get("exclude", "")
        self.set_placeholder = kwargs.get("set_placeholder", True)
        self.size = parse_size(kwargs.get("size", ""), default=SIZE_MD)
        self.horizontal_label_class = kwargs.get(
            "horizontal_label_class", get_bootstrap_setting("horizontal_label_class")
        )
        self.horizontal_field_class = kwargs.get(
            "horizontal_field_class", get_bootstrap_setting("horizontal_field_class")
        )
        self.checkbox_layout = kwargs.get("checkbox_layout", get_bootstrap_setting("checkbox_layout"))
        self.checkbox_style = kwargs.get("checkbox_style", get_bootstrap_setting("checkbox_style"))
        self.horizontal_field_offset_class = kwargs.get(
            "horizontal_field_offset_class", get_bootstrap_setting("horizontal_field_offset_class")
        )
        self.inline_field_class = kwargs.get("inline_field_class", get_bootstrap_setting("inline_field_class"))
        self.error_css_class = kwargs.get("error_css_class", None)
        self.required_css_class = kwargs.get("required_css_class", None)
        self.bound_css_class = kwargs.get("bound_css_class", None)
        self.alert_error_type = kwargs.get("alert_error_type", "non_fields")

    @property
    def is_floating(self):
        """Return whether to render `form-control` widgets as floating."""
        return self.layout == "floating"

    @property
    def is_horizontal(self):
        """Return whether to render form horizontally."""
        return self.layout == "horizontal"

    @property
    def is_inline(self):
        """Return whether to render widgets with inline layout."""
        return self.layout == "inline"

    def parse_size(self, size):
        """Return size if it is valid, default size if size is empty, or throws exception."""
        size = parse_size(size, default=DEFAULT_SIZE)
        if size == SIZE_XS:
            raise BootstrapError('Size "xs" is not valid for form controls.')
        return size

    def get_size_class(self, prefix):
        """Return size class for given prefix."""
        return get_size_class(self.size, prefix=prefix) if self.size in ["sm", "lg"] else ""

    def get_kwargs(self):
        """Return kwargs to pass on to child renderers."""
        context = {
            "layout": self.layout,
            "wrapper_class": self.wrapper_class,
            "field_class": self.field_class,
            "label_class": self.label_class,
            "show_help": self.show_help,
            "show_label": self.show_label,
            "exclude": self.exclude,
            "set_placeholder": self.set_placeholder,
            "size": self.size,
            "horizontal_label_class": self.horizontal_label_class,
            "horizontal_field_class": self.horizontal_field_class,
            "checkbox_layout": self.checkbox_layout,
            "checkbox_style": self.checkbox_style,
            "inline_field_class": self.inline_field_class,
            "error_css_class": self.error_css_class,
            "bound_css_class": self.bound_css_class,
            "required_css_class": self.required_css_class,
            "alert_error_type": self.alert_error_type,
        }
        return context

    def get_context_data(self):
        """Return context data for rendering."""
        return self.get_kwargs()

    def render(self):
        """Render to string."""
        return ""


class FormsetRenderer(BaseRenderer):
    """Default formset renderer."""

    def __init__(self, formset, *args, **kwargs):
        if not isinstance(formset, BaseFormSet):
            raise BootstrapError('Parameter "formset" should contain a valid Django Formset.')
        self.formset = formset
        super().__init__(*args, **kwargs)

    def get_context_data(self):
        context = super().get_context_data()
        context["formset"] = self.formset
        return context

    def render_management_form(self):
        """Return HTML for management form."""
        return text_value(self.formset.management_form)

    def render_forms(self):
        rendered_forms = mark_safe("")
        kwargs = self.get_kwargs()
        for form in self.formset.forms:
            rendered_forms += render_form(form, **kwargs)
        return rendered_forms

    def get_formset_errors(self):
        return self.formset.non_form_errors()

    def render_errors(self):
        formset_errors = self.get_formset_errors()
        if formset_errors:
            return render_template_file(
                "django_bootstrap5/form_errors.html",
                context={
                    "errors": formset_errors,
                    "form": self.formset,
                    "layout": self.layout,
                },
            )
        return mark_safe("")

    def render(self):
        return format_html(self.render_management_form() + "{}{}", self.render_errors(), self.render_forms())


class FormRenderer(BaseRenderer):
    """Default form renderer."""

    def __init__(self, form, *args, **kwargs):
        if not isinstance(form, BaseForm):
            raise BootstrapError('Parameter "form" should contain a valid Django Form.')
        self.form = form
        super().__init__(*args, **kwargs)

    def get_context_data(self):
        context = super().get_context_data()
        context["form"] = self.form
        return context

    def render_fields(self):
        rendered_fields = mark_safe("")
        kwargs = self.get_kwargs()
        for field in self.form:
            rendered_fields += render_field(field, **kwargs)
        return rendered_fields

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

        return mark_safe("")

    def render(self):
        errors = self.render_errors(self.alert_error_type)
        fields = self.render_fields()
        return errors + fields


class FieldRenderer(BaseRenderer):
    """Default field renderer."""

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

        self.placeholder = text_value(kwargs.get("placeholder", self.default_placeholder))

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

    @property
    def is_floating(self):
        return super().is_floating and self.can_widget_float(self.widget) and self.is_widget_form_control(self.widget)

    @property
    def default_placeholder(self):
        """Return default placeholder for field."""
        return self.field.label if get_bootstrap_setting("set_placeholder") else ""

    def restore_widget_attrs(self):
        self.widget.attrs = self.initial_attrs.copy()

    def is_widget_form_control(self, widget):
        """Return whether given widget is of type `form-control`."""
        return (isinstance(widget, Input) and not isinstance(widget, CheckboxInput)) or isinstance(widget, Textarea)

    def get_widget_input_type(self, widget):
        """Return input type of widget, or None."""
        return widget.input_type if isinstance(widget, Input) else None

    def can_widget_float(self, widget):
        """Return whether given widget can be set to `form-floating` behavior."""
        # TODO: Add support for select widgets, within Bootstrap 5 restrictions
        # TODO: Add support for textarea widgets
        # TODO: Check support for date, time and other types
        return (
            not isinstance(widget, FileInput)
            and self.is_widget_form_control(widget)
            and self.get_widget_input_type(widget) != "color"
        )

    def add_widget_class_attrs(self, widget=None):
        """Add class attribute to widget."""
        if widget is None:
            widget = self.widget
        size_prefix = None

        before = []
        classes = [widget.attrs.get("class", "")]
        if ReadOnlyPasswordHashWidget is not None and isinstance(widget, ReadOnlyPasswordHashWidget):
            before.append("form-control-static")
        elif self.is_widget_form_control(widget):
            before.append("form-control")
            if self.get_widget_input_type(widget) == "color":
                before.append("form-control-color")
            size_prefix = "form-control"
        elif isinstance(widget, Select):
            before.append("form-select")
            size_prefix = "form-select"
        elif isinstance(widget, CheckboxInput):
            before.append("form-check-input")

        if size_prefix:
            classes.append(get_size_class(self.size, prefix=size_prefix, skip=["xs", "md"]))

        if self.field.errors:
            if self.error_css_class:
                classes.append(self.error_css_class)
        elif self.field.form.is_bound:
            classes.append(self.success_css_class)

        classes = before + classes
        widget.attrs["class"] = merge_css_classes(*classes)

    def add_placeholder_attrs(self, widget=None):
        """Add placeholder attribute to widget."""
        if widget is None:
            widget = self.widget
        placeholder = widget.attrs.get("placeholder", self.placeholder)
        if placeholder and self.set_placeholder and is_widget_with_placeholder(widget):
            widget.attrs["placeholder"] = conditional_escape(strip_tags(placeholder))

    def add_widget_attrs(self):
        """Return HTML attributes for widget as dict."""
        if self.is_multi_widget:
            widgets = self.widget.widgets
        else:
            widgets = [self.widget]
        for widget in widgets:
            self.add_widget_class_attrs(widget)
            self.add_placeholder_attrs(widget)
            if isinstance(widget, (RadioSelect, CheckboxSelectMultiple)):
                widget.template_name = "django_bootstrap5/widgets/radio_select.html"
            elif isinstance(widget, ClearableFileInput):
                widget.template_name = "django_bootstrap5/widgets/clearable_file_input.html"

    def get_label_class(self, horizontal=False):
        """Return CSS class for label."""
        label_classes = [text_value(self.label_class)]
        if not self.show_label:
            label_classes.append("visually-hidden")
        else:
            if isinstance(self.widget, CheckboxInput):
                widget_label_class = "form-check-label"
            elif self.is_inline:
                widget_label_class = "visually-hidden"
            elif horizontal:
                widget_label_class = merge_css_classes(self.horizontal_label_class, "col-form-label")
            else:
                widget_label_class = "form-label"
            label_classes = [widget_label_class] + label_classes
        return merge_css_classes(*label_classes)

    def get_field_html(self):
        """Return HTML for field."""
        self.add_widget_attrs()
        field_html = self.field.as_widget(attrs=self.widget.attrs)
        self.restore_widget_attrs()
        return field_html

    def get_label_html(self, horizontal=False):
        """Return value for label."""
        label_html = "" if self.show_label == "skip" else self.field.label
        if label_html:
            label_html = render_label(
                label_html,
                label_for=self.field.id_for_label,
                label_class=self.get_label_class(horizontal=horizontal),
            )
        return label_html

    def get_help_html(self):
        """Return HTML for help text."""
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
        """Return HTML for field errors."""
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

    def get_inline_field_class(self):
        """Return CSS class for inline field."""
        return self.inline_field_class or "col-12"

    def get_checkbox_classes(self):
        """Return CSS classes for checkbox."""
        classes = ["form-check"]
        if self.checkbox_style == "switch":
            classes.append("form-switch")
        if self.checkbox_layout == "inline":
            classes.append("form-check-inline")
        return merge_css_classes(*classes)

    def get_wrapper_classes(self):
        """Return classes for wrapper."""
        wrapper_classes = [self.wrapper_class]
        if self.is_floating:
            wrapper_classes.append("form-floating")
        if self.field.errors:
            wrapper_classes.append(self.error_css_class)
        elif self.field.form.is_bound:
            wrapper_classes.append(self.success_css_class)
        if self.field.field.required:
            wrapper_classes.append(self.required_css_class)
        if self.is_inline:
            wrapper_classes.append(self.get_inline_field_class())
        else:
            if self.is_horizontal:
                wrapper_classes.append("row")
            wrapper_classes.append("mb-3")
        return merge_css_classes(*wrapper_classes)

    def field_before_label(self):
        """Return whether field should be placed before label."""
        return isinstance(self.widget, CheckboxInput) or self.is_floating

    def render(self):
        if self.field.name in self.exclude.replace(" ", "").split(","):
            return ""
        if self.field.is_hidden:
            return text_value(self.field)

        field = self.get_field_html()
        if self.field_before_label():
            label = self.get_label_html()
            field = field + label
            label = mark_safe("")
            horizontal_class = merge_css_classes(self.horizontal_field_class, self.horizontal_field_offset_class)
        else:
            label = self.get_label_html(horizontal=self.is_horizontal)
            horizontal_class = self.horizontal_field_class

        if isinstance(self.widget, CheckboxInput):
            field = format_html(
                '<div class="{form_check_class}">{field}</div>',
                form_check_class=self.get_checkbox_classes(),
                field=field,
            )

        field_with_help_and_errors = format_html("{}{}{}", field, self.get_help_html(), self.get_errors_html())
        if self.is_horizontal:
            field_with_help_and_errors = format_html(
                '<div class="{}">{}</div>', horizontal_class, field_with_help_and_errors
            )

        return format_html(
            '<{tag} class="{wrapper_classes}">{label}{field_with_help_and_errors}</{tag}>',
            tag=WRAPPER_TAG,
            wrapper_classes=self.get_wrapper_classes(),
            label=label,
            field_with_help_and_errors=field_with_help_and_errors,
        )
