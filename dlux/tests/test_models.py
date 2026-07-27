from django.test import SimpleTestCase

from dlux.models import BaseDluxRecord, ChildWork, Collection, Work


class TestBaseDluxRecord(SimpleTestCase):
    """Tests for custom functionality of BaseDluxRecord.

    Since django makes it awkward to declare new Models outside of models.py, this is tested using
    existing concrete subclasses.
    """

    def test_get_fields_with_parents(self) -> None:
        """BaseDluxModel.get_dlux_fields() returns DluxField objects for a model."""
        cases: list[tuple[type[BaseDluxRecord], bool, list[str]]] = [
            (Work, False, ["ark", "collection", "title", "description", "resource_type"]),
            (Work, True, ["collection"]),
            (Collection, True, []),
            (ChildWork, True, ["parent", "order"]),
        ]

        for model, exclude_parents, expected in cases:
            with self.subTest(model=model, exclude_parents=exclude_parents):
                result = model.get_dlux_fields(exclude_parents=exclude_parents)
                self.assertEqual(list(result.keys()), expected)
