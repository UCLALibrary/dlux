from django.contrib import admin

from dlux.models import ChildWork, Collection, Work

# TODO move this model-specific stuff to DluxField properties, generate the admins programmatically


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):  # pyright: ignore[reportMissingTypeArgument]
    pass


class ChildWorkInline(admin.StackedInline):  # pyright: ignore[reportMissingTypeArgument]
    model = ChildWork
    extra = 0


@admin.register(Work)
class WorkAdmin(admin.ModelAdmin):  # pyright: ignore[reportMissingTypeArgument]
    inlines = [ChildWorkInline]
