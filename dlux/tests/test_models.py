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
            "access_copy": dlux_fields.access_copy,
            "ark": dlux_fields.ark,
            "caption": dlux_fields.caption,
            "creator": dlux_fields.creator,
            "date_created": dlux_fields.date_created,
            "description": dlux_fields.description,
            "genre": dlux_fields.genre,
            "iiif_manifest_url": dlux_fields.iiif_manifest_url,
            "iiif_viewing_hint": dlux_fields.iiif_viewing_hint,
            "inscription": dlux_fields.inscription,
            "language": dlux_fields.language,
            "normalized_date": dlux_fields.normalized_date,
            "parent": dlux_fields.parent,
            "photographer": dlux_fields.photographer,
            "preservation_copy": dlux_fields.preservation_copy,
            "publisher": dlux_fields.publisher,
            "resource_type": dlux_fields.resource_type,
            "subject": dlux_fields.subject,
            "subject_topic": dlux_fields.subject_topic,
            "thumbnail_url": dlux_fields.thumbnail_url,
            "title": dlux_fields.title,
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
            "DateInfoFields": {
                "date_created": dlux_fields.date_created,
                "normalized_date": dlux_fields.normalized_date,
            },
            "DigitalAssetFields": {
                "access_copy": dlux_fields.access_copy,
                "iiif_manifest_url": dlux_fields.iiif_manifest_url,
                "iiif_viewing_hint": dlux_fields.iiif_viewing_hint,
                "preservation_copy": dlux_fields.preservation_copy,
                "thumbnail_url": dlux_fields.thumbnail_url,
            },
        }
        result = Work.get_dlux_fields(by_base_class=True)
        self.assertEqual(result, expected)
