from typing import cast

from bs4 import BeautifulSoup, Tag
from django.contrib.auth import get_user_model
from django.test import TestCase


class CollectionIntegrationTests(TestCase):
    def setUp(self) -> None:
        User = get_user_model()
        self.user = cast(
            User,
            User.objects.create_user(  # pyright: ignore[reportAttributeAccessIssue, reportUnknownMemberType]
                username="test",
                password="pwd",
                is_staff=True,
                is_superuser=True,
            ),
        )

    def test_new_collection_page(self) -> None:
        self.client.force_login(self.user)
        response = self.client.get("/dlux/collection/add/")
        self.assertEqual(response.status_code, 200)

        parsed = BeautifulSoup(response.text, features="html.parser")

        fieldsets = parsed.find_all("fieldset")
        named_fieldsets: dict[str, Tag] = {}
        for fs in fieldsets:
            if title := fs.find("h2"):
                named_fieldsets[title.text] = fs

        # Assertions about "Top Level" Fields

        self.assertIsNone(parsed.find("select", id="id_parent"))

        # Assertions about "Basic Descriptive Fields"

        arrayfield_widget = named_fieldsets["Basic Descriptive Fields"].find(
            "textarea",
            id="id_description",
        )
        self.assertIsNotNone(arrayfield_widget)  # for readable error message
        assert arrayfield_widget is not None  # for the type checker
        self.assertIn("data-django-jsonform", arrayfield_widget.attrs)

    def test_new_work_page(self) -> None:
        self.client.force_login(self.user)
        response = self.client.get("/dlux/work/add/")
        self.assertEqual(response.status_code, 200)

        parsed = BeautifulSoup(response.text, features="html.parser")

        fieldsets = parsed.find_all("fieldset")
        named_fieldsets: dict[str, Tag] = {}
        for fs in fieldsets:
            if title := fs.find("h2"):
                named_fieldsets[title.text] = fs

        # Assertions about "Top Level" Fields

        self.assertIsNotNone(parsed.find("select", id="id_parent"))
        label = fieldsets[0].find("label", attrs={"for": "id_parent"})
        assert label is not None
        self.assertEqual(label.text, "Collection:")
        self.assertIn("required", label.attrs["class"])

        # Assertions about "Basic Descriptive Fields"

        arrayfield_widget = named_fieldsets["Basic Descriptive Fields"].find(
            "textarea",
            id="id_description",
        )
        self.assertIsNotNone(arrayfield_widget)  # for readable error message
        assert arrayfield_widget is not None  # for the type checker
        self.assertIn("data-django-jsonform", arrayfield_widget.attrs)

    def test_invalid_normalized_date_shows_validation_message(self) -> None:
        self.client.force_login(self.user)
        response = self.client.post(
            "/dlux/collection/add/",
            data={
                "title": "Test Collection",
                "ark": "ark:/21198/z1234567",
                "normalized_date": '["foobar"]',  # invalid date
            },
        )
        self.assertContains(
            response,
            "Date must be in format YYYY, YYYY-MM, YYYY-MM-DD, or START_DATE/END_DATE.",
        )
