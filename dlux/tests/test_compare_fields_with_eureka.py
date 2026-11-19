import csv
import io

from django.test import SimpleTestCase

from dlux.management.commands.compare_fields_with_eureka import (
    build_comparison_report,
    normalize_field_name,
)


class TestNormalizeFieldName(SimpleTestCase):
    def test_normalization_ignores_case_whitespace_and_punctuation(self) -> None:
        """Test that normalization function ignores case, whitespace, and punctuation."""
        self.assertEqual(normalize_field_name("Local Identifier  "), "localidentifier")
        self.assertEqual(normalize_field_name("OPAC-url"), "opacurl")
        self.assertEqual(normalize_field_name("Alt.Title_other"), "alttitleother")

    def test_normalization_supports_likely_mapping_comparison(self) -> None:
        """Test that likely mappings are correctly identified based on normalization."""
        eureka_report = io.StringIO(
            "field_name,non_empty_values\nLocal Identifier  ,1\nOpac-url,1\n"
        )
        report = build_comparison_report(csv.DictReader(eureka_report))
        self.assertEqual(
            report["likely_mappings"],
            {
                "Local Identifier  ": "local_identifier",
                "Opac-url": "opac_url",
            },
        )
