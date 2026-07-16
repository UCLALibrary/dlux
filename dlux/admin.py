from django.contrib import admin

from dlux.models import Work


@admin.register(Work)
class WorkAdmin(admin.ModelAdmin[Work]):
    pass
