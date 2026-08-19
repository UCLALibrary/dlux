"""Django admin classes for dlux records.

Since dlux relies on the django admin site for its staff-facing interface, this file will define
most if not all of the user experience. The admin site documentation is very helpful: https://docs.djangoproject.com/en/5.2/ref/contrib/admin/

The django admin site allows for heavy customization and although in some cases this is seen as an
anti-pattern, dlux is not such a case. However, customization should be applied
programmatically based on the schema defined in dlux.dlux_fields, rather than explicitly. In other
words, avoid naming specific fields in this file – put that information in dlux.dlux_fields and find
a way to pull it in here.
"""

import re
from typing import Any, override

from django.contrib import admin
from django.db.models import Field
from django.forms.fields import Field as FormField
from django.http.request import HttpRequest

# Attempting to manually annotate the return type of ModelAdmin.get_fieldsets() runs into a lot of
# "incompatible override" errors; easiest to use the django-stubs FieldsetSpec type
from django_stubs_ext import FieldsetSpec  # pyright: ignore[reportPrivateUsage]

from dlux.models import ChildWork, Collection, Record, Work

#
#   Utility methods
#


def fieldsets_for_model(model: type[Record]) -> FieldsetSpec:
    """Use django fieldsets to group metadata fields in collapsable groups.

    The structure of the fieldsets is based on the grouping of fields into abstract models from
    which self.model inherits, as returned by BaseDluxRecord.get_dlux_fields().

    Returns:
        A nested data structure conforming to
        https://docs.djangoproject.com/en/6.0/ref/contrib/admin/#django.contrib.admin.ModelAdmin.fieldsets
    """
    dlux_fields = model.get_dlux_fields(by_base_class=True)

    fieldsets: FieldsetSpec = [
        (
            None,
            {"fields": list(dlux_fields.pop("Record").keys())},
        )
    ]

    for model_name, fields in dlux_fields.items():
        fieldsets.append(
            (
                re.sub(r"(?<!^)(?=[A-Z])", " ", model_name),  # Convert camel to title case
                {
                    "classes": ["collapse"],
                    "fields": list(fields.keys()),
                },
            )
        )

    return fieldsets


#
#   Admin classes
#


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin[Collection]):
    """Django admin for Collection records."""

    @override
    def get_fieldsets(
        self,
        request: HttpRequest,
        obj: Record | None = None,
    ) -> FieldsetSpec:
        return fieldsets_for_model(self.model)


class ChildWorkInline(admin.StackedInline[ChildWork, Work]):
    """Django admin inline for "childwork-level" records.

    At present (July 2026), there is only a single, generic "ChildWork" record supporting all
    metadata options. In the future we hope to have different models for different types, e.g. Page
    (of a Manuscript).
    """

    model = ChildWork
    extra = 0

    @override
    def get_fieldsets(
        self,
        request: HttpRequest,
        obj: Record | None = None,
    ) -> FieldsetSpec:
        return fieldsets_for_model(self.model)


@admin.register(Work)
class WorkAdmin(admin.ModelAdmin[Work]):
    """Django admin for "work-level" records.

    At present (July 2026), there is only a single, generic "Work" record supporting all metadata
    options. In the future we hope to use different models for different resource types, e.g.
    Manuscript or SimpleImage.
    """

    inlines = [ChildWorkInline]  # pyright: ignore[reportUnknownVariableType]

    @override
    def get_fieldsets(
        self,
        request: HttpRequest,
        obj: Record | None = None,
    ) -> FieldsetSpec:
        return fieldsets_for_model(self.model)

    @override
    def formfield_for_dbfield(
        self,
        db_field: Field[Any, Any],
        request: HttpRequest,
        **kwargs: Any,
    ) -> FormField | None:
        if db_field.name == "parent":
            kwargs.update(
                {
                    "required": True,
                    "label": "Collection",
                    "queryset": Collection.objects.all(),
                }
            )

        return super().formfield_for_dbfield(db_field, request, **kwargs)
