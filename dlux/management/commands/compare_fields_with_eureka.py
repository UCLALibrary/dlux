"""Compare CSV-derived fields on `dlux` Records with those in Eureka."""

import csv
import json
import string
from csv import DictReader
from pathlib import Path

from django.core.management.base import BaseCommand, CommandParser

from dlux.fields import DluxField
from dlux.models import Record

ComparisonReport = dict[str, dict[str, str] | list[str]]


def escape_markdown(text: str) -> str:
    """Escape punctuation so fields display correctly in Markdown."""
    return "".join(
        f"\\{character}" if character in string.punctuation else character for character in text
    )


def normalize_field_name(field_name: str) -> str:
    """Normalize provided field name for comparison purposes.

    Normalization removes case differences and non-alphanumeric characters from the field name.
    """
    return "".join(character for character in field_name.casefold() if character.isalnum())


def get_dlux_csv_aliases(field: DluxField) -> list[str]:
    """Return a DluxField's static (i.e. non-callable) CSV aliases."""
    return [] if callable(field.csv) else field.csv


def build_comparison_report(
    eureka_report_data: DictReader[str],
) -> ComparisonReport:
    """Build a comparison report between Eureka fields and dlux fields.

    Eureka field names are the keys in each mapping group, and each known or
    likely mapping points to a single canonical DluxField name.

    Args:
        eureka_report_data: Data loaded from the Eureka CSV report.

    Return:
        A dictionary containing the comparison report with the following keys:
          - "known_mappings": Eureka fields with known DluxField mapping from CSV aliases.
          - "likely_mappings": Eureka fields with likely DluxField mapping, based on normalization.
          - "human_review": Eureka fields that require human review due to ambiguity.
          - "empty_eureka_fields": Empty Eureka fields (no non-empty values).
    """
    dlux_fields: dict[str, DluxField] = Record.get_dlux_fields(by_base_class=False)

    # There may be multiple rows with the same Eureka field name but different non-empty counts,
    # so we aggregate them here to avoid ignoring field names that should be considered non-empty.
    eureka_field_value_counts: dict[str, int] = {}
    for row in eureka_report_data:
        field_name = row["field_name"]
        non_empty_values = int(row["non_empty_values"])
        eureka_field_value_counts[field_name] = (
            eureka_field_value_counts.get(field_name, 0) + non_empty_values
        )
    # Now based on the aggregated counts, we can determine which Eureka fields are truly empty.
    empty_eureka_fields: set[str] = {
        field_name
        for field_name, non_empty_values in eureka_field_value_counts.items()
        if non_empty_values == 0
    }
    # Then we can remove the empty Eureka fields from consideration for mappings.
    eureka_field_names: set[str] = set(eureka_field_value_counts) - empty_eureka_fields

    # Initialize report groups for later.
    known_mappings: dict[str, str] = {}
    likely_mappings: dict[str, str] = {}
    human_review: dict[str, str] = {}

    for eureka_field_name in sorted(eureka_field_names):
        # Look for known mappings based on CSV aliases on DluxFields.
        alias_matches: set[str] = {
            field_name
            for field_name, field in dlux_fields.items()
            if eureka_field_name in get_dlux_csv_aliases(field)
        }

        # Each Eureka field should match only one known DluxField via CSV alias.
        # If there is more than one, it requires human review.
        if len(alias_matches) == 1:
            known_mappings[eureka_field_name] = next(iter(alias_matches))
            continue
        if len(alias_matches) > 1:
            human_review[eureka_field_name] = ""
            continue

        # Ignore punctuation, whitespace, and case to look for likely mappings
        normalized_matches = {
            field_name
            for field_name, field in dlux_fields.items()
            # Match to canonical DluxField name...
            if normalize_field_name(eureka_field_name) == normalize_field_name(field_name)
            # ...or any of its CSV aliases.
            or any(
                normalize_field_name(eureka_field_name) == normalize_field_name(alias)
                for alias in get_dlux_csv_aliases(field)
            )
        }
        if len(normalized_matches) == 1:
            likely_mappings[eureka_field_name] = next(iter(normalized_matches))
        else:
            human_review[eureka_field_name] = ""

    return {
        "known_mappings": known_mappings,
        "likely_mappings": likely_mappings,
        "human_review": human_review,
        "empty_eureka_fields": sorted(empty_eureka_fields),
    }


def format_comparison_report(report: ComparisonReport, output_format: str) -> str:
    """Return a formatted comparison report as a string."""
    if output_format == "json":
        return json.dumps(report, indent=4)

    output_lines = ["# Eureka field comparison", ""]
    for group_name, group in report.items():
        # Add a section header for each group with its name and count,
        # e.g. "## Known Mappings (Count: 5)"
        output_lines.extend([f"## {group_name.replace('_', ' ').title()} (Count: {len(group)})"])

        if isinstance(group, dict):
            for eureka_field_name, dlux_field_name in group.items():
                escaped_eureka_field_name = escape_markdown(eureka_field_name)
                if dlux_field_name:
                    output_lines.append(
                        f"- {escaped_eureka_field_name}: {escape_markdown(dlux_field_name)}"
                    )
                else:
                    output_lines.append(f"- {escaped_eureka_field_name}")
        else:
            output_lines.extend(f"- {escape_markdown(field_name)}" for field_name in group)

        if not group:
            output_lines.append("_None._")

        # Add a blank line after each group for readability
        output_lines.append("")
    return "\n".join(output_lines).rstrip()


class Command(BaseCommand):
    """Management command entry-point."""

    help = "Generate a comparison report between Eureka fields and `dlux` fields."

    def add_arguments(self, parser: CommandParser) -> None:
        """CLI args for management command."""
        parser.add_argument(
            "-i",
            "--eureka_report_path",
            type=str,
            default="scripts/eureka_fields_report/reports/eureka_fields.csv",
            help=(
                "Path to the Eureka fields report CSV file. "
                "Default: `scripts/eureka_fields_report/reports/eureka_fields.csv`"
            ),
        )
        parser.add_argument(
            "-o",
            "--output",
            type=str,
            default=None,
            help="Path to write report (default: stdout)",
        )
        parser.add_argument(
            "-f",
            "--format",
            choices=["json", "markdown"],
            default="json",
            help="Format of the output report (default: json)",
        )

    def handle(self, *args: object, **options: object) -> None:
        """Command handler."""
        eureka_report_path = Path(str(options["eureka_report_path"]))
        if not eureka_report_path.exists():
            raise FileNotFoundError(f"Eureka report not found: {eureka_report_path}")

        with open(eureka_report_path) as f:
            eureka_report_data = csv.DictReader(f)
            report = build_comparison_report(eureka_report_data=eureka_report_data)

        formatted_report = format_comparison_report(report, output_format=str(options["format"]))

        if options["output"]:
            output_path = Path(str(options["output"]))
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, "w") as f:
                f.write(formatted_report)
        else:
            self.stdout.write(formatted_report)
