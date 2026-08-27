import re

from django.test import SimpleTestCase

from dlux.dlux_fields import NORMALIZED_DATE_REGEX


class TestNormalizedDateRegexPattern(SimpleTestCase):
    def test_regex_pattern(self) -> None:
        """Test that NORMALIZED_DATE_REGEX matches valid inputs and does not match invalid ones.

        NOTE: This test case is intended to cover the NORMALIZED_DATE_REGEX pattern,
        used as the first-pass validator for `normalized_dates`.
        The regex pattern does not catch all known invalid edge cases,
        such as impossible dates or ranges where the end date is before the start date. (HR 8/25/26)
        """

        regex = re.compile(NORMALIZED_DATE_REGEX)

        valid_dates = [
            "2023",  # YYYY
            "2023-01",  # YYYY-MM
            "2023-01-01",  # YYYY-MM-DD
            "-2000",  # negative year
            "750",  # 3-digit year
            "2023/2024",  # year range
            "2023-01/2023-12",  # year-month range
            "2023-01-01/2023-12-31",  # year-month-day range
            "750/751",  # 3-digit year range
            "-750/-650",  # negative year range
        ]

        invalid_dates = [
            "foobar",  # non-numeric
            "2020/2022/2023",  # too many parts in range
            "23",  # too few digits in year
        ]

        for date in valid_dates:
            with self.subTest(date=date):
                self.assertTrue(regex.match(date), f"Valid date '{date}' did not match regex.")

        for date in invalid_dates:
            with self.subTest(date=date):
                self.assertFalse(regex.match(date), f"Invalid date '{date}' matched regex.")


# class TestNormalizedDateValidator(SimpleTestCase):
#     """Test that `normalized_date_validator` correctly validates normalized date strings
#     and raises ValidationError for invalid inputs.

#     NOTE: `normalized_date_validator` is not currently used in `dlux_fields.py`.
#     It is intended as a second-pass validator for `normalized_date` fields,
#     to catch edge cases not covered by the NORMALIZED_DATE_REGEX. (HR 8/25/26)
#     """

#     def test_valid_dates(self) -> None:
#         valid_dates = [
#             "2023",  # YYYY
#             "2023-01",  # YYYY-MM
#             "2023-01-01",  # YYYY-MM-DD
#             "-2000",  # negative year
#             "750",  # 3-digit year
#             "2023/2024",  # year range
#             "2023-01/2023-12",  # range with months
#             "2023-01-01/2023-12-31",  # range with full dates
#             "750/751",  # range with 3-digit years
#             "-750/-650",  # valid negative year range
#             "-100/100",  # range spans negative to positive year
#         ]
#         for date in valid_dates:
#             with self.subTest(date=date):
#                 try:
#                     normalized_date_validator(date)
#                 except Exception as e:
#                     self.fail(f"Validator raised an exception for valid date '{date}': {e}")

#     def test_invalid_dates(self) -> None:
#         invalid_dates = [
#             "2023-13",  # invalid month
#             "2023-01-32",  # invalid day
#             "2023/2022",  # end date before start date
#             "abc",  # non-numeric
#             "2023-01-01/2022-12-31",  # start date after end date
#             "-1300/-1400",  # negative year range out of order
#             "100/-100",  # range cannot span positive to negative year
#         ]
#         for date in invalid_dates:
#             with self.subTest(date=date):
#                 with self.assertRaises(ValidationError):
#                     normalized_date_validator(date)
