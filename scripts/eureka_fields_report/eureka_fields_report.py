"""A basic Python script that scans the CSV files in your local Eureka repo and builds a report.

For each column name found across all files, it shows how many files use that column,
how many non-empty values it contains, how many distinct values exist,
the length of the longest value,
and whether it uses the multi-value delimiter.
"""

import csv
import json
import sys
from collections import defaultdict
from io import TextIOWrapper
from pathlib import Path

# Constants - change as needed
SCAN_DIRS = {"checked_out", "in_progress", "done", "metadata_reload"}
DELIM = "|~|"

# Input
def resolve_root(argv: list[str] | None = None) -> Path:
    """Asks user to provide absolute path to local Eureka repo."""
    argv = sys.argv[1:] if argv is None else argv
    if argv:
        folder = argv[0].strip()
    else:
        folder = input("\nEnter the path to your local eureka repo: ").strip()
    return Path(folder).resolve()


def get_reports_dir() -> Path:
    """Creates a reports directory if one does not already exist."""
    reports_dir = Path(__file__).resolve().parent / "reports"
    reports_dir.mkdir(exist_ok=True)
    return reports_dir


# CSV encoding detection
def open_text(path: Path) -> TextIOWrapper:
    """Detects encoding of a file.

    If the encoding is not UTF-8, lists the encoding and filename.

    Returns a file object for reading the file,
    with correct encoding set.
    """
    with open(path, "rb") as f:
        head = f.read(4096)
    if head.startswith(b"\xff\xfe") or head.startswith(b"\xfe\xff"):
        print(f"\n[utf-16] {path}", file=sys.stderr)
        return open(path, "r", encoding="utf-16", errors="replace", newline="")
    if b"\x00" in head:
        print(f"\n[utf-16-le] {path}", file=sys.stderr)
        return open(path, "r", encoding="utf-16-le", errors="replace", newline="")
    return open(path, "r", encoding="utf-8-sig", errors="replace", newline="")


# Scanning repo
def find_csv_files(root: Path, scan_dirs: set[str] = SCAN_DIRS) -> list[Path]:
    """Returns all CSV files under the SCAN_DIRS constants."""
    return [
        path
        for path in root.rglob("*.csv")
        if path.relative_to(root).parts[0] in scan_dirs
    ]

def new_stats() -> dict:
    """Data from scan will be collected into these accumulators."""
    return {
        "file_count": defaultdict(int),
        "nonempty": defaultdict(int),
        "uniq_vals": defaultdict(set),
        "max_len": defaultdict(int),
        "has_delim": defaultdict(bool),
        "files_by_field": defaultdict(list),
    }


def scan_csv(path: Path, stats: dict, delim: str = DELIM) -> None:
    """Reads a single CSV file and updates the shared stats dictionaries."""
    file_count = stats["file_count"]
    nonempty = stats["nonempty"]
    uniq_vals = stats["uniq_vals"]
    max_len = stats["max_len"]
    has_delim = stats["has_delim"]
    files_by_field = stats["files_by_field"]

    with open_text(path) as f:
        reader = csv.reader(f)
        header = next(reader, None)
        if header is None:
            return  # empty file - nothing to count
        for field in set(header):
            files_by_field[field].append(str(path))
            file_count[field] += 1
        for row in reader:
            for field, value in zip(header, row):
                value = value.strip()
                if not value:
                    continue
                nonempty[field] += 1
                uniq_vals[field].add(value)
                max_len[field] = max(max_len[field], len(value))
                if delim in value:
                    has_delim[field] = True


def scan_all(csv_files: list[Path], delim: str = DELIM) -> dict:
    """Scans CSV files and returns aggregated stats.

    This is the single home for scan policy: the progress message,
    the per-file loop, and error handling all live here.
    """
    stats = new_stats()
    print(f"\nScanning {len(csv_files)} csv files", file=sys.stderr)
    for path in csv_files:
        try:
            scan_csv(path, stats, delim=delim)
        except Exception as e:
            print(f"[error] {path}: {e}", file=sys.stderr)
    return stats


# Reports
def write_field_report(stats: dict, out_path: Path) -> None:
    """Writes the CSV field report to out_path."""
    file_count = stats["file_count"]
    nonempty = stats["nonempty"]
    uniq_vals = stats["uniq_vals"]
    max_len = stats["max_len"]
    has_delim = stats["has_delim"]
    sorted_fields = sorted(file_count)

    with open(out_path, "w", newline="", encoding="utf-8") as report:
        writer = csv.writer(report)
        writer.writerow(
            [
                "field_name",
                "files_with_field",
                "non_empty_values",
                "distinct_values",
                "max_value_length",
                "uses_delimiter",
            ]
        )
        for field in sorted_fields:
            writer.writerow(
                [
                    field,
                    file_count[field],
                    nonempty[field],
                    len(uniq_vals[field]),
                    max_len[field],
                    "yes" if has_delim[field] else "no",
                ]
            )


def write_file_index(stats: dict, out_path: Path) -> None:
    """Writes the JSON file mapping each field to the files that use it."""
    sorted_fields = sorted(stats["file_count"])
    with open(out_path, "w", encoding="utf-8") as json_file:
        json.dump(
            {field: sorted(stats["files_by_field"][field]) for field in sorted_fields},
            json_file,
            indent=2,
        )


def main(argv: list[str] | None = None) -> None:
    """Scans CSVs in the repo and writes the field report and file index."""
    root = resolve_root(argv)
    reports_dir = get_reports_dir()

    csv_files = find_csv_files(root)
    stats = scan_all(csv_files, delim=DELIM)

    csv_out = reports_dir / "eureka_fields.csv"
    json_out = reports_dir / "eureka_files.json"
    write_field_report(stats, csv_out)
    write_file_index(stats, json_out)

    print(
        f"\nDone! Scanned {len(csv_files)} files in {root}. "
        f"{csv_out.name} & {json_out.name} were saved to {reports_dir}",
        file=sys.stderr,
    )


if __name__ == "__main__":
    main()