"""Django models for dlux.

Our data model is defined in dlux-specific FieldGroup and DluxField objects, which should probably
be moved outside the standard django file structure. Django models are then created programmatically
from those objects.
"""

from dataclasses import dataclass
from typing import Any, Callable, Iterable, TypeVar, cast

from django.apps import apps
from django.db.models import (
    CharField,
    Field,
    Model,
    TextField,
)
from django_jsonform.models.fields import (  # pyright: ignore[reportMissingTypeStubs]
    ArrayField as BaseArrayField,
)

#
#   Base dataclass for schema fields
#

SetType = TypeVar("SetType")
GetType = TypeVar("GetType")


class ArrayField(BaseArrayField[SetType, GetType]):
    """Extended version of django.contrib.postgres.ArrayField.

    django_jsonform extends the base field to support json schemas.
    Here we extend django_jsonform's ArrayField to build different schemas
    depending on the base_field's type and attributes.
    """

    base_field: Field[Any, Any]

    def formfield(self, **kwargs: Any) -> Any:  # noqa: ANN401
        """Retreive django FormField class.

        Modifies django_jsonform behavior based on the base_field's type and attributes.
        """
        # If the base_field is a CharField or TextField with choices,
        # set the choices on the schema from the field's choices
        # and use a multiselect widget.
        if (
            not kwargs.get("schema")
            and (isinstance(self.base_field, CharField) or isinstance(self.base_field, TextField))
            and self.base_field.choices
        ):
            kwargs["schema"] = {
                "type": "list",  # or 'array'
                "items": {
                    "type": "string",
                    "choices": [
                        {"title": label, "value": id} for id, label in self.base_field.choices
                    ],
                    "widget": "multiselect",
                },
            }

        # Pass through the base_field's validators to the ArrayField's formfield,
        # so that they display in the admin UI if any item with the array fails validation.
        if not kwargs.get("base_field"):
            kwargs["base_field"] = self.base_field.formfield(validators=self.base_field.validators)

        return super().formfield(**kwargs)  # pyright: ignore[reportUnknownVariableType, reportUnknownMemberType]


@dataclass
class DluxField:
    """Container for Django classes and other information related to a dlux metadata term.

    Args:
        django: An instance of (a subclass of) django.db.models.Field.
        csv: A list of csv column aliases to import into the field.
        solr: A list of solr field names to which the field should be indexed.
        exclude_models: A tuple of names of models in which the field is not used. At a database
            level, all models are stored as `Record` and contain all fields, but fields will only
            be shown in the admin interface of a proxy model if that model or its superclass is not
            included in `exclude_models`. The default is an empty tuple, which shows the field for
            all model types.
    """

    django: "Field[Any, Any]"
    csv: list[str]
    solr: list[str] | Callable[[Model], dict[str, Any]]
    exclude_models: Iterable[str] = tuple()

    def get_exclude_models(self) -> tuple[type[Model], ...]:
        """Return a tuple of python classes for each model named in self.exclude_models."""
        # django-stubs's return type of get_model() is `type[Any]`, but we know it's `type[Model]``
        return tuple(
            cast(type[Model], apps.get_model("dlux", name)) for name in self.exclude_models
        )
