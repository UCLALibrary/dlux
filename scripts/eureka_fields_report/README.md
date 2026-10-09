# Eureka CSV Fields Report

A basic Python script that scans the CSV files in your local Eureka repo and builds a report. For each column name found across all files, it shows how many files use that column, how many non-empty values it contains, how many distinct values exist, the length of the longest value, and whether it uses the multi-value delimiter.


## Requirements

- Python 3.7 or newer

## How to run it

1. Run:
   ```
   python eureka_fields_report.py
   ```
1. Prompt will ask for full path to your local Eureka repo and press Enter. 
- e.g.: `/Users/geno/Documents/eureka`

## Configuration

Two settings are at the top of the script:

- **`SCAN_DIRS`**: the folder names to scan within eureka. Add or remove folder names as needed. 
  - Default is `checked_out`, `in_progress`, `done`, and `metadata_reload`.
- **`DELIM`**: the multi-value delimiter to look for inside cells. 
  - Default is `|~|`.

## Reports

Two files are created in the `reports` folder:

### 1. `eureka_fields.csv`

One row per unique field name, with these columns:

- `field_name`: The exact column name as it appears in the CSV headers
- `files_with_field`: For each column name, how many files had that column
- `non_empty_values`: For each column name, how many cells had values.
- `distinct_values`: For each column name, count how many distinct values
- `max_value_length`: For each column name, the length of the longest value seen
- `uses_delimiter`: For each column name, "yes" if any value contains the `|~|` delimiter

### 2. `eureka_files.json`

A JSON file that maps each field name to a sorted list of file paths where that field appears.


## Areas for improvement

- **Duplicate column names**. Columns are deduped for `files_with_field`, but their values
  may still get counted twice for other columns.

- **Memory**. It holds every distinct value in memory while counting, so big repos
  are going to use a lot of RAM. Should be fine for eureka, but likely wont scale.

- **Row length mismatches**. If a row has fewer cells than the header, the missing
  ones just count as empty. Extra cells get silently dropped. No warning right
  now.
