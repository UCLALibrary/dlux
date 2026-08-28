from django.test import SimpleTestCase

from dlux.admin import fieldsets_for_model
from dlux.models import ChildWork, Collection, Work


class TestFieldsetsForModel(SimpleTestCase):
    def test_includes_all_abstract_models(self) -> None:
        result = [fs[0] for fs in fieldsets_for_model(Collection)]
        expected = [None, "Basic Descriptive Fields", "Date Info Fields", "Digital Asset Fields"]

        self.assertEqual(result, expected)

    def test_collection_no_parent(self) -> None:
        result = fieldsets_for_model(Collection)

        assert len(result) >= 1  # guard for the type checker
        self.assertNotIn("parent", result[0][1]["fields"])

    def test_work_has_parent(self) -> None:
        result = fieldsets_for_model(Work)

        assert len(result) >= 1  # guard for the type checker
        self.assertIn("parent", result[0][1]["fields"])

    def test_childwork_has_parent(self) -> None:
        result = fieldsets_for_model(ChildWork)

        assert len(result) >= 1  # guard for the type checker
        self.assertIn("parent", result[0][1]["fields"])
