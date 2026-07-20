from dataclasses import dataclass, field
from typing import Any

from django.contrib.postgres.fields import ArrayField
from django.db.models import Field, ForeignKey, Model, TextField
from django.db.models.fields import CharField


@dataclass
class DluxExtra:
    csv: list[str] = field(default_factory=list[str])
    solr: list[str] = field(default_factory=list[str])


class MappedCharField(CharField):  # pyright: ignore[reportMissingTypeArgument]
    dlux_extra: DluxExtra

    def __init__(
        self,
        verbose_name: str,
        *,
        max_length: int = 2000,
        null: bool = False,
        blank: bool = False,
        choices: list[tuple[str, str]],
        primary_key: bool = False,
        unique: bool = False,
        dlux_extra: DluxExtra = DluxExtra(),
    ) -> None:
        super().__init__(
            max_length=max_length,
            verbose_name=verbose_name,
            null=null,
            blank=blank,
            choices=choices,
            primary_key=primary_key,
            unique=unique,
        )
        self.dlux_extra = dlux_extra


class MappedTextField(TextField):  # pyright: ignore[reportMissingTypeArgument]
    dlux_extra: DluxExtra

    # Defaults for standa
    max_length = 2000
    null = False

    def __init__(
        self,
        verbose_name: str,
        *,
        null: bool = False,
        blank: bool = False,
        unique: bool = False,
        dlux_extra: DluxExtra = DluxExtra(),
    ) -> None:
        super().__init__(
            verbose_name=verbose_name,
            null=null,
            blank=blank,
            unique=unique,
        )
        self.dlux_extra = dlux_extra


class MappedArrayField(ArrayField):  # pyright: ignore[reportMissingTypeArgument]
    dlux_extra: DluxExtra

    def __init__(
        self,
        base_field: "Field[Any, Any]",
        *,
        verbose_name: str | None = None,
        null: bool = False,
        blank: bool = False,
        unique: bool = False,
        dlux_extra: DluxExtra = DluxExtra(),
    ) -> None:
        super().__init__(
            base_field=base_field,
            verbose_name=verbose_name,
            null=null,
            blank=blank,
            unique=unique,
            dlux_extra=dlux_extra,
        )
        self.dlux_extra = dlux_extra


class MappedForeignKey(ForeignKey):  # pyright: ignore[reportMissingTypeArgument]
    dlux_extra: DluxExtra

    def __init__(
        self,
        to: type[Model] | str,
        *,
        verbose_name: str | None = None,
        null: bool = False,
        blank: bool = False,
        unique: bool = False,
        dlux_extra: DluxExtra = DluxExtra(),
    ) -> None:
        super().__init__(
            to,
            verbose_name=verbose_name,
            null=null,
            blank=blank,
            unique=unique,
        )
        self.dlux_extra = dlux_extra
