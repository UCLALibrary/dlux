"""Django admin classes for dlux records.

Since dlux relies on the django admin site for its staff-facing interface, this file will define
most if not all of the user experience. The admin site documentation is very helpful: https://docs.djangoproject.com/en/5.2/ref/contrib/admin/

The django admin site allows for heavy customization and although in some cases this is seen as an
anti-pattern, dlux is not such a case. However, customization should be applied
programmatically based on the schema defined in dlux.dlux_fields, rather than explicitly. In other
words, avoid naming specific fields in this file – put that information in dlux.dlux_fields and find
a way to pull it in here.
"""

from django.contrib import admin

from dlux.models import ChildWork, Collection, Work


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):  # pyright: ignore[reportMissingTypeArgument]
    """Django admin for Collection records."""

    pass


class ChildWorkInline(admin.StackedInline):  # pyright: ignore[reportMissingTypeArgument]
    """Django admin inline for "childwork-level" records.

    At present (July 2026), there is only a single, generic "ChildWork" record supporting all
    metadata options. In the future we hope to have different models for different types, e.g. Page
    (of a Manuscript).
    """

    model = ChildWork
    extra = 0


@admin.register(Work)
class WorkAdmin(admin.ModelAdmin):  # pyright: ignore[reportMissingTypeArgument]
    """Django admin for "work-level" records.

    At present (July 2026), there is only a single, generic "Work" record supporting all metadata
    options. In the future we hope to use different models for different resource types, e.g.
    Manuscript or SimpleImage.
    """

    inlines = [ChildWorkInline]
