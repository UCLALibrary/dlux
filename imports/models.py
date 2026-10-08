from datetime import datetime

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db.models import (
    PROTECT,
    DateTimeField,
    FileField,
    ForeignKey,
    Model,
    PositiveIntegerField,
)


class CSVImport(Model):
    file = FileField()

    rows = PositiveIntegerField[int, int](null=True, blank=True)
    imported_at = DateTimeField[datetime, datetime](auto_now_add=True)
    imported_by = ForeignKey[AbstractUser, AbstractUser](
        to=get_user_model(),
        null=True,
        blank=True,
        on_delete=PROTECT,
    )

    def __str__(self) -> str:
        return f"{self.pk}: {self.file.name}"
