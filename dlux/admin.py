from django.contrib import admin

from dlux.models import Collection, Work


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):  # pyright: ignore[reportMissingTypeArgument]
    pass


@admin.register(Work)
class WorkAdmin(admin.ModelAdmin):  # pyright: ignore[reportMissingTypeArgument]
    pass
