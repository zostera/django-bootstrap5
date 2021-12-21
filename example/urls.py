from django.urls import re_path

from app.views import (
    DefaultFormByFieldView,
    DefaultFormsetView,
    DefaultFormView,
    FormHorizontalView,
    FormInlineView,
    FormWithFilesView,
    HomePageView,
    MiscView,
    PaginationView,
)

urlpatterns = [
    re_path(r"^$", HomePageView.as_view(), name="home"),
    re_path(r"^formset$", DefaultFormsetView.as_view(), name="formset_default"),
    re_path(r"^form$", DefaultFormView.as_view(), name="form_default"),
    re_path(r"^form_by_field$", DefaultFormByFieldView.as_view(), name="form_by_field"),
    re_path(r"^form_horizontal$", FormHorizontalView.as_view(), name="form_horizontal"),
    re_path(r"^form_inline$", FormInlineView.as_view(), name="form_inline"),
    re_path(r"^form_with_files$", FormWithFilesView.as_view(), name="form_with_files"),
    re_path(r"^pagination$", PaginationView.as_view(), name="pagination"),
    re_path(r"^misc$", MiscView.as_view(), name="misc"),
]
