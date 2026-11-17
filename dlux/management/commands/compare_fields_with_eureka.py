"""Compare CSV-derived fields on `dlux` Records with those in Eureka."""

import csv

from django.core.management.base import BaseCommand, CommandParser

from dlux.models import Record


def print_comparison_group(group_title: str, fields: set[str]) -> None:
    """Print a comparison group with its title and fields using Markdown."""
    print(f"## {group_title} (count: {len(fields)})")
    for field in sorted(fields):  # sort fields alphabetically
        print(f"- `{field}`")
    print()  # empty line between groups


def compare_fields_with_eureka(
    eureka_field_names: set[str], dlux_csv_field_names: set[str]
) -> None:
    """Compare CSV-derived fields on `dlux` Records with those in Eureka."""
    common_fields = eureka_field_names & dlux_csv_field_names
    only_in_eureka = eureka_field_names - dlux_csv_field_names
    only_in_dlux = dlux_csv_field_names - eureka_field_names

    print_comparison_group("Common Fields", common_fields)
    print_comparison_group("Only in Eureka", only_in_eureka)
    print_comparison_group("Only in Dlux", only_in_dlux)


class Command(BaseCommand):
    """Management command entry-point."""

    help = "Compare CSV-derived fields on `dlux` Records with those in Eureka."

    def add_arguments(self, parser: CommandParser) -> None:
        """CLI args for management command."""
        parser.add_argument(
            "-i",
            "--eureka_report_path",
            type=str,
            default="scripts/eureka_fields_report/reports/eureka_fields.csv",
            help="Path to the Eureka fields report CSV file",
        )

    def handle(self, *args: object, **options: object) -> None:
        """Command handler: get field name sets for Eureka and `dlux`, then compare."""
        # Load Eureka field names from the CSV report
        eureka_report_path: str = str(options["eureka_report_path"])
        with open(eureka_report_path) as f:
            eureka_report_data = csv.DictReader(f)
            eureka_field_names = {row["field_name"] for row in eureka_report_data}

        # Retrieve CSV-derived field names from `dlux` Records
        dlux_csv_field_names: set[str] = {
            name
            for field in Record.get_dlux_fields(by_base_class=False).values()
            # Type checker complains because `field.csv` might be a callable, so check that it's not
            if not callable(field.csv)
            for name in field.csv
        }

        compare_fields_with_eureka(
            eureka_field_names=eureka_field_names,
            dlux_csv_field_names=dlux_csv_field_names,
        )
