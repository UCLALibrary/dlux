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

    def test_new_collection_page_contains_unsortedfields_fieldset(self) -> None:
        self.client.force_login(self.user)
        response = self.client.get("/dlux/collection/add/")
        self.assertEqual(response.status_code, 200)

        parsed = BeautifulSoup(response.text)

        fieldsets = parsed.find_all("fieldset")
        named_fieldsets: dict[str, Tag] = {}
        for fs in fieldsets:
            if title := fs.find("h2"):
                named_fieldsets[title.text] = fs

        arrayfield_widget = named_fieldsets["UnsortedFields"].find("textarea", id="id_description")
        self.assertIsNotNone(arrayfield_widget)  # for readable error message
        assert arrayfield_widget is not None  # for the type checker
        self.assertIn("data-django-jsonform", arrayfield_widget.attrs)
