from django.test import SimpleTestCase

from dlux import dlux_fields
from dlux.models import (
    Work,
)


class TestBaseDluxRecord(SimpleTestCase):
    """Tests for custom functionality of BaseDluxRecord.

    Since django makes it awkward to declare new Models outside of models.py, this is tested using
    existing concrete subclasses.
    """

    def test_get_dlux_fields(self) -> None:
        """BaseDluxModel.get_dlux_fields() returns DluxField objects for a model."""

        result = Work.get_dlux_fields(by_base_class=False)
        expected = {
            "ark": dlux_fields.ark,
            "collection": dlux_fields.collection,
            "title": dlux_fields.title,
            "description": dlux_fields.description,
            "resource_type": dlux_fields.resource_type,
        }
        self.assertEqual(result, expected)

    maxDiff = 2000

    def test_get_dlux_fields_by_base_class(self) -> None:
        """BaseDluxModel.get_dlux_fields() returns DluxField objects for a model."""
        expected = {
            "Work": {"collection": dlux_fields.collection},
            "BaseDluxRecord": {
                "ark": dlux_fields.ark,
                "title": dlux_fields.title,
                "resource_type": dlux_fields.resource_type,
            },
            "UnsortedFields": {"description": dlux_fields.description},
        }
        result = Work.get_dlux_fields(by_base_class=True)
        self.assertEqual(result, expected)
