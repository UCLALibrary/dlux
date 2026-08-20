"""Validators for use on model fields."""

import re
from datetime import datetime

from dateutil import parser
from dateutil.parser import ParserError
from django.core.exceptions import ValidationError

DATE_PATTERN = r"-?\d?\d\d\d(-\d\d){0,2}"


def _is_valid_date(date_str: str) -> None:
    """Check if the given string represents a valid date or date range.

    Args:
        date_str (str): The date string to validate.

    Raises:
        ValidationError: If the date string is not valid.
    """
    parts = date_str.split("/")
    if len(parts) > 2:
        raise ValidationError(
            "Date ranges must be in the format START_DATE/END_DATE. "
            "They cannot have more than two parts."
        )
    parsed_dates: list[datetime] = []
    for part in parts:
        if part.isdigit() and len(part) == 3:
            part = part.zfill(4)  # Pad 3-digit years with leading zero for parser
        try:
            parsed_date: datetime = parser.parse(part)  # type: ignore
            parsed_dates.append(parsed_date)
        # If either part cannot be parsed, raise ValidationError.
        except ParserError:
            raise ValidationError("The provided date string(s) could not be parsed to valid dates.")
    # If there are two dates, ensure the first is not after the second.
    if len(parsed_dates) == 2 and parsed_dates[0] > parsed_dates[1]:
        raise ValidationError("In a date range, the start date must not be after the end date.")


def _matches_regex(value: str) -> None:
    """Validate that the input value matches the expected normalized date format using regex.

    Args:
        value (str): The input string to validate.

    Raises:
        ValidationError: If the input string does not match the expected format.
    """
    regex = rf"^{DATE_PATTERN}(/{DATE_PATTERN})?$"
    message = (
        "Date must be in format YYYY, YYYY-MM, YYYY-MM-DD, or START_DATE/END_DATE. "
        "Supports 3-digit (but not fewer) and negative years, e.g. 750 or -1750 ."
    )

    if not re.match(regex, value):
        raise ValidationError(message)


def normalized_date_validator(value: str) -> None:
    """Validate that the input string is a valid normalized date format.

    This validator checks if the input string is in one of the following formats:
    - YYYY
    - YYYY-MM
    - YYYY-MM-DD
    - START_DATE/END_DATE (where both dates are in one of the above formats)

    It also supports 3-digit years (but not fewer) and negative years, e.g., 0750 or -0750.

    Args:
        value (str): The date string to validate.
    """
    try:
        _matches_regex(value)
        _is_valid_date(value)
    except ValidationError as validation_error:
        raise validation_error
