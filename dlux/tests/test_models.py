from django.test import SimpleTestCase

from dlux import dlux_fields
from dlux.models import Work


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
            "parent": dlux_fields.parent,
            "title": dlux_fields.title,
            "caption": dlux_fields.caption,
            "creator": dlux_fields.creator,
            "description": dlux_fields.description,
            "genre": dlux_fields.genre,
            "inscription": dlux_fields.inscription,
            "language": dlux_fields.language,
            "photographer": dlux_fields.photographer,
            "publisher": dlux_fields.publisher,
            "resource_type": dlux_fields.resource_type,
            "subject": dlux_fields.subject,
            "subject_topic": dlux_fields.subject_topic,
        }
        self.assertEqual(result, expected)

    maxDiff = None

    def test_get_dlux_fields_by_base_class(self) -> None:
        """BaseDluxModel.get_dlux_fields() returns DluxField objects for a model."""
        expected = {
            "Record": {
                "parent": dlux_fields.parent,
                "ark": dlux_fields.ark,
                "title": dlux_fields.title,
            },
            "BasicDescriptiveFields": {
                "caption": dlux_fields.caption,
                "creator": dlux_fields.creator,
                "description": dlux_fields.description,
                "genre": dlux_fields.genre,
                "inscription": dlux_fields.inscription,
                "language": dlux_fields.language,
                "photographer": dlux_fields.photographer,
                "publisher": dlux_fields.publisher,
                "resource_type": dlux_fields.resource_type,
                "subject": dlux_fields.subject,
                "subject_topic": dlux_fields.subject_topic,
            },
        }
        result = Work.get_dlux_fields(by_base_class=True)
        self.assertEqual(result, expected)
