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
            "archival_collection_box": dlux_fields.archival_collection_box,
            "archival_collection_folder": dlux_fields.archival_collection_folder,
            "archival_collection_number": dlux_fields.archival_collection_number,
            "archival_collection_title": dlux_fields.archival_collection_title,
            "ark": dlux_fields.ark,
            "caption": dlux_fields.caption,
            "creator": dlux_fields.creator,
            "date_created": dlux_fields.date_created,
            "description": dlux_fields.description,
            "finding_aid_url": dlux_fields.finding_aid_url,
            "funding_note": dlux_fields.funding_note,
            "genre": dlux_fields.genre,
            "iiif_manifest_url": dlux_fields.iiif_manifest_url,
            "iiif_viewing_hint": dlux_fields.iiif_viewing_hint,
            "inscription": dlux_fields.inscription,
            "language": dlux_fields.language,
            "local_identifier": dlux_fields.local_identifier,
            "local_rights_statement": dlux_fields.local_rights_statement,
            "normalized_date": dlux_fields.normalized_date,
            "opac_url": dlux_fields.opac_url,
            "parent": dlux_fields.parent,
            "photographer": dlux_fields.photographer,
            "preservation_copy": dlux_fields.preservation_copy,
            "program": dlux_fields.program,
            "publisher": dlux_fields.publisher,
            "repository": dlux_fields.repository,
            "resource_type": dlux_fields.resource_type,
            "rights_country": dlux_fields.rights_country,
            "rights_statement": dlux_fields.rights_statement,
            "services_contact": dlux_fields.services_contact,
            "subject_topic": dlux_fields.subject_topic,
            "subject": dlux_fields.subject,
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
            "LibraryInfoFields": {
                "archival_collection_box": dlux_fields.archival_collection_box,
                "archival_collection_folder": dlux_fields.archival_collection_folder,
                "archival_collection_number": dlux_fields.archival_collection_number,
                "archival_collection_title": dlux_fields.archival_collection_title,
                "finding_aid_url": dlux_fields.finding_aid_url,
                "funding_note": dlux_fields.funding_note,
                "local_identifier": dlux_fields.local_identifier,
                "local_rights_statement": dlux_fields.local_rights_statement,
                "opac_url": dlux_fields.opac_url,
                "program": dlux_fields.program,
                "repository": dlux_fields.repository,
                "rights_country": dlux_fields.rights_country,
                "rights_statement": dlux_fields.rights_statement,
                "services_contact": dlux_fields.services_contact,
            },
        }
        result = Work.get_dlux_fields(by_base_class=True)
        self.assertEqual(result, expected)
