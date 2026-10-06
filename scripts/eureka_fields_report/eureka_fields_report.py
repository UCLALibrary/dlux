import csv
import json
import sys
from pathlib import Path
from collections import defaultdict

# Constants - change as needed
SCAN_DIRS = {"checked_out", "in_progress", "done", "metadata_reload"}
DELIM = "|~|"


# Checks for non utf-8 files and lists them
def open_text(path):
    with open(path, "rb") as f:
        head = f.read(4096)
    if head.startswith(b"\xff\xfe") or head.startswith(b"\xfe\xff"):
        print(f"\n[utf-16] {path}", file=sys.stderr)
        return open(path, "r", encoding="utf-16", errors="replace", newline="")
    if b"\x00" in head:
        print(f"\n[utf-16-le] {path}", file=sys.stderr)
        return open(path, "r", encoding="utf-16-le", errors="replace", newline="")
    return open(path, "r", encoding="utf-8-sig", errors="replace", newline="")


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv

    if argv:
        folder = argv[0].strip()
    else:
        folder = input("\nEnter the path to your local eureka repo: ").strip()
    root = Path(folder).resolve()

    script_dir = Path(__file__).resolve().parent
    reports_dir = script_dir / "reports"
    reports_dir.mkdir(exist_ok=True)

    file_count = defaultdict(int)
    nonempty = defaultdict(int)
    uniq_vals = defaultdict(set)
    max_len = defaultdict(int)
    has_delim = defaultdict(bool)
    files_by_field = defaultdict(list)

    csv_files = [
        path for path in root.rglob("*.csv")
        if path.relative_to(root).parts[0] in SCAN_DIRS
    ]

    print(f"\nScanning {len(csv_files)} csv files in {root}", file=sys.stderr)
    for path in csv_files:
        with open_text(path) as f:
            reader = csv.reader(f)
            header = next(reader)
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
                    if DELIM in value:
                        has_delim[field] = True

    sorted_fields = sorted(file_count.keys())

    csv_out = reports_dir / "eureka_fields.csv"
    with open(csv_out, "w", newline="", encoding="utf-8") as report:
        writer = csv.writer(report)
        writer.writerow([
            "field_name", "files_with_field", "non_empty_values",
            "distinct_values", "max_value_length", "uses_delimiter"
        ])
        for field in sorted_fields:
            writer.writerow([
                field,
                file_count[field],
                nonempty[field],
                len(uniq_vals[field]),
                max_len[field],
                "yes" if has_delim[field] else "no",
            ])

    json_out = reports_dir / "eureka_files.json"
    with open(json_out, "w", encoding="utf-8") as json_file:
        json.dump(
            {field: sorted(files_by_field[field]) for field in sorted_fields},
            json_file,
            indent=2,
        )

    print(f"\nDone! {csv_out.name} & {json_out.name} were saved to {reports_dir}", file=sys.stderr)


if __name__ == "__main__":
    main()