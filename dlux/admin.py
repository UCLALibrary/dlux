"""Django admin classes for dlux records.

Since dlux relies on the django admin site for its staff-facing interface, this file will define
most if not all of the user experience. The admin site documentation is very helpful: https://docs.djangoproject.com/en/5.2/ref/contrib/admin/

The django admin site allows for heavy customization and although in some cases this is seen as an
anti-pattern, dlux is not such a case. However, customization should be applied
programmatically based on the schema defined in dlux.dlux_fields, rather than explicitly. In other
words, avoid naming specific fields in this file – put that information in dlux.dlux_fields and find
a way to pull it in here.
"""

from typing import TYPE_CHECKING, Never

from django.contrib import admin
from django.http.request import HttpRequest

from dlux.models import BaseDluxRecord, ChildWork, Collection, Work

if TYPE_CHECKING:
    from django.contrib.admin.options import (
        _FieldOpts,  # pyright: ignore[reportPrivateUsage]
        _FieldsetSpec,  # pyright: ignore[reportPrivateUsage]
    )
    from django.utils.functional import _StrPromise  # pyright: ignore[reportPrivateUsage]


@admin.register(Collection)
class BaseDluxAdmin(admin.ModelAdmin[BaseDluxRecord]):
    """Django admin for Collection records."""

    def get_fieldsets(
        self,
        request: HttpRequest,
        obj: BaseDluxRecord | None = None,
    ) -> """list[tuple[str | _StrPromise | None, _FieldOpts]]
        | tuple[tuple[str | _StrPromise | None, _FieldOpts], ...]
        | tuple[Never]""":
        """Use django fieldsets to group metadata fields in collapsable groups.

        See https://docs.djangoproject.com/en/6.0/ref/contrib/admin/#django.contrib.admin.ModelAdmin.fieldsets

        The structure of the fieldsets is based on the grouping of fields into abstract models from
        which self.model inherits, as returned by BaseDluxRecord.get_dlux_fields().
        """
        dlux_fields = self.model.get_dlux_fields(by_base_class=True)

        fieldsets: "_FieldsetSpec" = [
            (
                None,
                {
                    "fields": [
                        *dlux_fields.pop("BaseDluxRecord", dict()).keys(),
                        *dlux_fields.pop(self.model.__name__, dict()).keys(),
                    ]
                },
            )
        ]

        for cls, fields in dlux_fields.items():
            fieldsets.append(
                (
                    cls,
                    {
                        "classes": ["collapse"],
                        "fields": list(fields.keys()),
                    },
                )
            )

        return fieldsets


class ChildWorkInline(admin.StackedInline[ChildWork, Work]):
    """Django admin inline for "childwork-level" records.

    At present (July 2026), there is only a single, generic "ChildWork" record supporting all
    metadata options. In the future we hope to have different models for different types, e.g. Page
    (of a Manuscript).
    """

    model = ChildWork
    extra = 0


@admin.register(Work)
class WorkAdmin(BaseDluxAdmin):
    """Django admin for "work-level" records.

    At present (July 2026), there is only a single, generic "Work" record supporting all metadata
    options. In the future we hope to use different models for different resource types, e.g.
    Manuscript or SimpleImage.
    """

    inlines = [ChildWorkInline]  # pyright: ignore[reportUnknownVariableType]
