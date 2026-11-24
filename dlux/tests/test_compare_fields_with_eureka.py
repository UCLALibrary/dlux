import csv
import io

from django.test import SimpleTestCase

from dlux.management.commands.compare_fields_with_eureka import (
    build_comparison_report,
    format_comparison_report,
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

    def test_markdown_report_escapes_special_characters_in_field_names(self) -> None:
        """Test that the Markdown report escapes special characters."""
        report = {
            "likely_mappings": {
                "[Binding note]": "binding_note",
                "**Field**  with ~punctuation~ |": "`value_with_backtick`",
            },
            "human_review": {"[Unmapped]": ""},
            "empty_eureka_fields": ["[Empty]"],
        }
        expected_lines = [
            r"- \[Binding note\]: binding\_note",
            r"- \*\*Field\*\*  with \~punctuation\~ \|: \`value\_with\_backtick\`",
            r"- \[Unmapped\]",
            r"- \[Empty\]",
        ]

        markdown = format_comparison_report(report, output_format="markdown")

        with self.subTest():
            for line in expected_lines:
                self.assertIn(line, markdown)
