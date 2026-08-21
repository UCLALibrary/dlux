from django.core.exceptions import ValidationError
from django.test import SimpleTestCase

from dlux.dlux_fields import normalized_date_validator


# NOTE: `normalized_date_validator` is not currently used in `dlux_fields.py`.
# The tests below are provided for future use, covering known edge cases. (HR 8/21/26)
class TestNormalizedDateValidator(SimpleTestCase):
    def test_valid_dates(self) -> None:
        valid_dates = [
            "2023",  # YYYY
            "2023-01",  # YYYY-MM
            "2023-01-01",  # YYYY-MM-DD
            "-2000",  # negative year
            "750",  # 3-digit year
            "2023/2024",  # year range
            "2023-01/2023-12",  # range with months
            "2023-01-01/2023-12-31",  # range with full dates
            "750/751",  # range with 3-digit years
            "-750/-650",  # valid negative year range
            "-100/100",  # range spans negative to positive year
        ]
        for date in valid_dates:
            with self.subTest(date=date):
                try:
                    normalized_date_validator(date)
                except Exception as e:
                    self.fail(f"Validator raised an exception for valid date '{date}': {e}")

    def test_invalid_dates(self) -> None:
        invalid_dates = [
            "2023-13",  # invalid month
            "2023-01-32",  # invalid day
            "2023/2022",  # end date before start date
            "abc",  # non-numeric
            "2023-01-01/2022-12-31",  # start date after end date
            "-1300/-1400",  # negative year range out of order
            "100/-100",  # range cannot span positive to negative year
        ]
        for date in invalid_dates:
            with self.subTest(date=date):
                with self.assertRaises(ValidationError):
                    normalized_date_validator(date)
