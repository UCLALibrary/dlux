"""Base classes for a field-first organization, with associated tools."""

# TODO: rename this file util.py or something that isn't part of the normal django file structure

import itertools
from dataclasses import dataclass, field
from typing import Any, Callable, Generator

from django.db.models import BaseConstraint, Field, Model


@dataclass
class DluxField:
    """Container for Django classes and other information related to a dlux metadata term."""

    django: "Field[Any, Any]"
    csv: list[str] | Callable[[dict[str, Any]], dict[str, Any]]
    solr: list[str] | Callable[[Model], dict[str, Any]]


@dataclass
class FieldGroupConfig:
    """Extra configuration for a FieldGroup.

    Included data will be injected into django into a django model or other relevant object.

    Attributes:
        db_constraints: A list of django database constraint objects. See https://docs.djangoproject.com/en/5.2/ref/models/constraints/.

    Example:
        from django.models import UniqueConstraint

        class CongressionalDistrict(FieldGroup):
            config = FieldGroupConfig(
                db_constraints = [
                    UniqueConstraint(fields=["state", "number"], name="unique_number_per_state"),
                ],
            )

            state = DluxField(...)
            number = DluxField(...)
    """

    db_constraints: list[BaseConstraint] = field(default_factory=list[BaseConstraint])


class FieldGroup:
    """Container for Groups of related fields, which can be added to django models.

    Uses a class-based syntax for readability and similarity to Django abstract classes, but is
    mostly equivalent to `dict[str, DluxField]`. Field groups should be defined as subclasses of
    FieldGroup, with individual fields as attributes of type DluxField.

    Attributes:
    config: A FieldGroupConfig object.

    Example:
        from django.db.models import CharField, IntegerField

        class CharacterMetadata(FieldGroup):
            name = DluxField(
                django = CharField(max_length=200),
                csv = ["Name"],
                solr = ["name_tesi"],
            )

            age = DluxField(
                django = IntegerField(),
                csv = ["Age"],
                solr = ["age_isi"],
            )
    """

    config: FieldGroupConfig = FieldGroupConfig()

    @classmethod
    def fields(cls) -> Generator[tuple[str, DluxField]]:
        """Generator functon to iterate over fields defined in a FieldGroup subclass.

        Yields:
            (name, field) tuples where `name` is a string and `field` is a DLuxField object.
        """
        for name, field in cls.__dict__.items():
            if isinstance(field, DluxField):
                yield name, field


# I'm (AW) not sure a decorator is appropriate here, but I haven't come up with anything better.
def with_field_groups(
    *groups: type[FieldGroup],
) -> Callable[[type[Model]], type[Model]]:
    """Decorator used to add a FieldGroup class to a django model.

    Example:
        from django.db.models import CharField, Model


        class GroupOne(FieldGroup):
            a = DluxField(django=CharField(...), ...)

        class GroupTwo(FieldGroup):
            b = DluxField(django=CharField(...), ...)

        @with_field_groups(GroupOne, GroupTwo)
        class MyModel(Model):
            pass

    Creates the same Django model as:
        from django.db.models import CharField, Model

        class MyModel(Model):
            a = CharField(...)
            b = CharField(...)
    """

    def decorator(cls: "type[Model]") -> "type[Model]":
        for group in groups:
            for name, field in itertools.chain(group.fields()):
                cls.add_to_class(name, field.django)

            cls._meta.constraints.extend(group.config.db_constraints)

        return cls

    return decorator
