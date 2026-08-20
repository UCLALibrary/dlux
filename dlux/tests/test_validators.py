from django.core.exceptions import ValidationError
from django.test import SimpleTestCase

from dlux.validators import normalized_date_validator


class TestNormalizedDateValidator(SimpleTestCase):
    def test_valid_dates(self) -> None:
        valid_dates = [
            "2023",
            "2023-01",
            "2023-01-01",
            "-0077",
            "0750",
            "2023/2024",
            # "-0077/-0076",
            "0750/0751",
        ]
        for date in valid_dates:
            with self.subTest(date=date):
                try:
                    normalized_date_validator(date)
                except Exception as e:
                    self.fail(f"Validator raised an exception for valid date '{date}': {e}")

    def test_invalid_dates(self) -> None:
        invalid_dates = [
            "2023-13",  # Invalid month
            "2023-01-32",  # Invalid day
            "2023/2022",  # End date before start date
            "abc",  # Non-numeric
            "2023-01-01/2022-12-31",  # End date before start date
        ]
        for date in invalid_dates:
            with self.subTest(date=date):
                with self.assertRaises(ValidationError):
                    normalized_date_validator(date)
