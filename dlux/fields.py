"""Django models for dlux.

Our data model is defined in dlux-specific FieldGroup and DluxField objects, which should probably
be moved outside the standard django file structure. Django models are then created programmatically
from those objects.
"""

from dataclasses import dataclass
from typing import Any, Callable

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


class ArrayField(BaseArrayField):
    """Extended version of django.contrib.postgres.ArrayField.

    django_jsonform extends the base field to support json schemas.
    Here we extend django_jsonform's ArrayField to build different schemas
    depending on the base_field's type and attributes.
    """

    base_field: Field[Any, Any]
    widget: str | None

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
        # Otherwise, use the widget set on the ArrayField
        elif not kwargs.get("schema") and self.widget:
            kwargs["schema"] = {
                "type": "list",
                "items": {
                    "type": "string",
                    "widget": self.widget,
                },
            }
        return super().formfield(**kwargs)  # pyright: ignore[reportUnknownVariableType, reportUnknownMemberType]


@dataclass
class DluxField:
    """Container for Django classes and other information related to a dlux metadata term."""

    django: "Field[Any, Any]"
    csv: list[str] | Callable[[dict[str, Any]], dict[str, Any]]
    solr: list[str] | Callable[[Model], dict[str, Any]]
