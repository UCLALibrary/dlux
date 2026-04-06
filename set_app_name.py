import argparse
from pathlib import Path


def _get_arguments() -> argparse.Namespace:
    """Parse command line arguments.

    :return: Parsed arguments."""

    parser = argparse.ArgumentParser(
        description="Rename a template Django application to a real name."
    )
    parser.add_argument(
        "--new_app_name", help="New name for the Django application", required=True
    )
    return parser.parse_args()


def _convert_to_pascal_case(input: str) -> str:
    """Convert a string to PascalCase.

    :param input: Value to be converted.
    :return output: Converted value.
    """

    # input may be in snake_case or kebab-case; replace underscores and hyphens with space,
    # temporarily, so words are still separated by spaces.
    tmp = input.replace("_", " ").replace("-", " ")
    # Capitalize the first letter of each word, then remove spaces.
    output = tmp.title().replace(" ", "")
    return output


def main() -> None:
    args = _get_arguments()

    # Not intended to be used with anything except placeholder application
    # from our template repository!
    # Map old (placeholder) names to new names.
    old_app_name = "my_app_name"
    new_app_name = args.new_app_name
    name_map = {
        old_app_name: new_app_name,
        _convert_to_pascal_case(old_app_name): _convert_to_pascal_case(new_app_name),
    }

    # Capture messages about changed files.
    messages = []

    # Capture name of this script, so we can skip it below.
    this_script = Path(__file__).name

    # Search through all python files and replace old name with new name.
    for python_file in Path().rglob("*.py"):
        # Skip the current script!
        if python_file.name == this_script:
            continue
        changed = False
        file_contents = python_file.read_text(encoding="utf-8")
        for search_text, replace_text in name_map.items():
            if search_text in file_contents:
                file_contents = file_contents.replace(search_text, replace_text)
                changed = True
                messages.append(
                    f"Changed {search_text} to {replace_text} in {python_file}"
                )
        if changed:
            python_file.write_text(file_contents, encoding="utf-8")
    for message in messages:
        print(message)

    # Finally, rename the placeholder directory.
    old_dir = Path(old_app_name)
    old_dir.rename(new_app_name)
    print(f"Renamed directory {old_app_name} to {new_app_name}")


if __name__ == "__main__":
    main()
