from typing import TYPE_CHECKING, Any, Literal, override

from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.http import HttpRequest

from dlux.importer import import_csv

from .models import CSVImport

if TYPE_CHECKING:
    from django.contrib.admin.options import (
        _FieldGroups as FieldGroups,  # pyright: ignore[reportPrivateUsage]  # noqa: F401
    )

GetFieldsType = (
    list[str | list[str] | tuple[str, ...] | tuple[()]]
    | tuple[str | list[str] | tuple[str, ...] | tuple[()], ...]
    | tuple[()]
)


@admin.register(CSVImport)
class CSVImportAdmin(ModelAdmin[CSVImport]):
    fields = [
        "file",
        "imported_at",
        "imported_by",
        "rows",
        "currently_in_library",
        "failures",
    ]
    list_display = [
        "__str__",
        "imported_at",
        "imported_by",
        # "rows",
        # "currently_in_library",
        # "failures",
    ]

    # def get_fields(self, request, obj=...):
    # def get_fields(self, request, obj):
    @override
    def get_fields(
        self,
        request: HttpRequest,
        obj: Any | None = ...,
    ) -> "FieldGroups":
        if obj:  # obj is not None, so this is an edit
            return super().get_fields(request=request, obj=obj)
        else:  # This is an new item
            return ["file"]

    @override
    def has_change_permission(
        self,
        request: HttpRequest,
        obj: Any | None = ...,
    ) -> Literal[False]:
        """Records of CSV imports cannot be changed once created."""
        return False

    @override
    def has_delete_permission(
        self,
        request: HttpRequest,
        obj: Any | None = ...,
    ) -> Literal[False]:
        """Records of CSV imports cannot be deleted once created."""
        return False

    @override
    def save_model(
        self,
        request: HttpRequest,
        obj: CSVImport,
        form: Any,
        change: Any,
    ) -> None:
        obj.imported_by = request.user
        super().save_model(request, obj, form, change)

        import_csv(obj.file.path)
