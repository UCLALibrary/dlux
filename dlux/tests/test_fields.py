from __future__ import annotations

from django.db.models import CharField, IntegerField
from django.test import SimpleTestCase

from dlux.fields import ArrayField


class TestArrayField(SimpleTestCase):
    def test_formfield_builds_schema_from_charfield_choices(self) -> None:
        array_field = ArrayField(
            base_field=CharField[str, str](
                max_length=5,
                choices=[
                    ("a", "A"),
                    ("b", "B"),
                ],
            ),
            size=None,
        )

        form_field = array_field.formfield()
        self.assertEqual(
            form_field.schema,
            {
                "type": "list",
                "items": {
                    "type": "string",
                    "choices": [
                        {"title": "A", "value": "a"},
                        {"title": "B", "value": "b"},
                    ],
                    "widget": "multiselect",
                },
            },
        )

    def test_formfield_keeps_existing_schema(self) -> None:

        array_field = ArrayField(
            base_field=CharField(
                max_length=5,
                choices=[
                    ("a", "A"),
                ],
            ),
            size=None,
        )
        custom_schema = {"type": "custom"}

        form_field = array_field.formfield(schema=custom_schema)

        self.assertEqual(form_field.schema, custom_schema)

    def test_formfield_does_not_build_schema_for_non_charfield(self) -> None:
        array_field = ArrayField(base_field=IntegerField(), size=None)

        form_field = array_field.formfield()

        self.assertIsNone(form_field.schema)
