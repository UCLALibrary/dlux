import itertools
from dataclasses import dataclass, field
from typing import Any, Callable, Generator

from django.db.models import BaseConstraint, Field, Model


@dataclass
class DluxField:
    django: "Field[Any, Any]"
    csv: list[str] | Callable[[dict[str, Any]], dict[str, Any]]
    solr: list[str] | Callable[[Model], dict[str, Any]]


@dataclass
class FieldGroupConfig:
    db_constraints: list[BaseConstraint] = field(default_factory=list[BaseConstraint])


class FieldGroup:
    """
    Parent for classes defining of related fields, which can be added to django models.

    Uses a class-based syntax for readability and similarity to Django abstract classes, but is
    equivalent to `TypedDict[str, DluxField]`.

    Example:
    >>> from django.db.models import CharField, IntegerField, Model

    >>> from dlux.fields import DluxField, FieldGroup, with_field_groups


    >>> class CharacterMetadata(FieldGroup):
    >>>     name = DluxField(
    >>>         django = CharField(max_length=200),
    >>>         csv = ["Name"],
    >>>         solr = ["name_tesi"],
    >>>     )

    >>> class MinionMetadata(FieldGroup):
    >>>     n_eyes = DluxField(
    >>>         django = IntegerField(),
    >>>         csv = ["Eyes"],
    >>>         solr = ["eyes_isi"],
    >>>     )

    >>> @with_field_groups(CharacterMetadata, MinionMetadata)
    >>> class Minion(Model):
    >>>     # Don't need this in practice, only here since we're not in models.py
    >>>     class Meta:
    >>>         app_label="dlux"

    >>> james = Minion(name="James", n_eyes=1)
    >>> james.name
    "James"

    >>> james.n_eyes
    1

    >>> james._meta.get_fields()
    (<django.db.models.fields.BigAutoField: id>, <django.db.models.fields.CharField: name>,
    <django.db.models.fields.IntegerField: n_eyes>)
    """

    config: FieldGroupConfig = FieldGroupConfig()

    @classmethod
    def fields(cls) -> Generator[tuple[str, DluxField]]:
        for name, field in cls.__dict__.items():
            if isinstance(field, DluxField):
                yield name, field


def with_field_groups(
    *fields: type[FieldGroup],
) -> Callable[[type[Model]], type[Model]]:
    """Decorator used to add a FieldGroup class to a django model."""

    def decorator(cls: "type[Model]") -> "type[Model]":
        for group in fields:
            for name, item in itertools.chain(group.fields()):
                cls.add_to_class(name, item.django)

            cls._meta.constraints.extend(group.config.db_constraints)

        return cls

    return decorator
