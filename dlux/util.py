"""General utilities for dlux."""

from typing import cast

from django.apps import apps
from django.db.models import Model


def get_model(name: str) -> type[Model]:
    """Given a name, return the django Model object defined in dlux.models.

    A wrapper around django.app.app.get_model(). Narrows the overly-broad `Any` return type from
    django-stubs.
    """
    return cast(type[Model], apps.get_model("dlux", name))
