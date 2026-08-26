"""Import records from CSV files."""

import csv
import re
from typing import Any

from django.db.models import CharField, Field, ForeignKey, IntegerField, ManyToManyField, TextField

from dlux.fields import ArrayField
from dlux.models import ChildWork, Collection, Record, Work

# used in parse_marc
MARC_SYMBOL = re.compile(r" \$[a-z] ")
MARC_SYMBOL_INITIAL_OR_FINAL = re.compile(r"(^\$[a-z] )|( \$[a-z]$)")

BaseField = CharField[str, str] | TextField[str, str] | IntegerField[str, str]


CREATED_RECORD_DEFAULTS: dict[str, Any] = {
    # Will need to add generic values for required fields
}

DLUX_FIELDS = Record.get_dlux_fields()
CSV_ALIAS_MAP: dict[str, str] = {
    alias: field_name
    for field_name, dlux_field in Record.get_dlux_fields().items()
    for alias in dlux_field.csv
}


def import_csv(csv_path: str) -> None:
    with open(csv_path, mode="r", encoding="utf-8") as file:
        column_headers = next(file).split(",")
        field_names = [CSV_ALIAS_MAP.get(header, header) for header in column_headers]

        # TODO: check for duplicate headers (check if duplicate *after* mapping, but report headers
        # from *before* mapping)

        for record in csv.DictReader(file, fieldnames=field_names):
            import_record(record)


def import_record(record: dict[str | Any, str | Any]) -> None:
    model = {
        "Collection": Collection,
        "Work": Work,
        "ChildWork": ChildWork,
    }[record["Object Type"]]

    mapped_data = {
        name: map_field(django_field=DLUX_FIELDS[name].django, input=value)
        for name, value in record
    }

    model.objects.update_or_create(
        ark=mapped_data.pop("ark"),
        # NOTE: I'm pretty sure the "defaults" data actually overwrites data in existing records,
        # but we should confirm this.
        defaults=mapped_data,
    )


def map_field(
    django_field: Field[Any, Any], input: str, _inner: bool = False
) -> str | Record | list[str] | list[Record]:
    """Parse UCLA-specific formatting of input strings.

    Args:
        django_field: A django field object. Used to determine the correct parsing rules.

        input: The string to be parsed, from a csv cell.

    Returns:
        For single-valued fields, a string in which UCLA representations of MARC symbols have been
        replaced with a space (most fields) or a double-dash separator (subject fields).

        For multi-valued fields, a list of such strings.
    """
    match django_field:
        case ArrayField() as array_field if isinstance(
            array_field.base_field,
            TextField | CharField,
        ):
            return [
                parse_string(
                    array_field.base_field,
                    item,
                )
                for item in input.split("|~|")
            ]

        case ArrayField():
            return input.split("|~|")

        case ManyToManyField() as field if issubclass(field.model, Record):
            return [
                Record.objects.get_or_create(
                    ark=item,
                    defaults=CREATED_RECORD_DEFAULTS,
                )[0]
                for item in input.split("|~|")
            ]

        case TextField() | CharField():
            return parse_string(django_field, input)

        case ForeignKey() as field if isinstance(field.model, Record):
            return Record.objects.get_or_create(ark=input, defaults=CREATED_RECORD_DEFAULTS)[0]

        case _:
            raise ValueError(f"Unable to map field {django_field}: unknown field type.")


def parse_string(django_field: Field[str, str], input: str) -> str:
    """Parse UCLA-specific formatting of input strings.

    Args:
        django_field: A django field object. Used to determine the correct parsing rules.

        input: The string to be parsed, from a csv cell.

    Returns:
        For single-valued fields, a string in which UCLA representations of MARC symbols have been
        replaced with a space (most fields) or a double-dash separator (subject fields).

        For multi-valued fields, a list of such strings.
    """
    marc_symbol_replacement = "--" if "subject" in django_field.name else " "
    parsed = MARC_SYMBOL.sub(marc_symbol_replacement, input)
    parsed = MARC_SYMBOL_INITIAL_OR_FINAL.sub("", parsed).strip()

    return parsed
