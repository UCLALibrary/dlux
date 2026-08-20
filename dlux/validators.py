"""Validators for use on model fields."""

from django.core.validators import RegexValidator

DATE_PATTERN = r"-?\d?\d\d\d(-\d\d){0,2}"
normalized_date_validator = RegexValidator(
    regex=rf"^{DATE_PATTERN}(/{DATE_PATTERN})?$",
    message="Date must be in format YYYY, YYYY-MM, YYYY-MM-DD, or START_DATE/END_DATE. "
    "Supports 3-digit and negative years, e.g. 0750 or -0077.",
)
