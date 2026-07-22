from django.test import SimpleTestCase


class PlaceholderTest(SimpleTestCase):
    """Placeholder to be deleted once we add real tests.

    Added when setting up unittest in github actions, but apparently it fails
    if no tests actually exist.
    """

    def test_nothing(self) -> None:
        """Return a successful result when setting up CI tests.

        Running unittest without any actual tests exits with an error status, so this is here to
        help us get github actions set up.
        """
        return
