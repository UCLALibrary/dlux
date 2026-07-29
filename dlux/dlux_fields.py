"""Django models for dlux.

Our data model is defined in dlux-specific FieldGroup and DluxField objects, which should probably
be moved outside the standard django file structure. Django models are then created programmatically
from those objects.
"""

from dataclasses import dataclass
from typing import Any, Callable

from django.contrib.postgres.fields import ArrayField
from django.db.models import (
    CASCADE,
    PROTECT,
    CharField,
    Field,
    ForeignKey,
    IntegerField,
    Model,
    TextField,
)

#
#   Base dataclass for schema fields
#


@dataclass
class DluxField:
    """Container for Django classes and other information related to a dlux metadata term."""

    django: "Field[Any, Any]"
    csv: list[str] | Callable[[dict[str, Any]], dict[str, Any]]
    solr: list[str] | Callable[[Model], dict[str, Any]]


#
#   Definitions for dlux fields
#

ark = DluxField(
    django=CharField(unique=True, blank=False, max_length=2000),
    csv=["Item ARK"],
    solr=["ark_ssi"],
)

collection = DluxField(
    django=ForeignKey(
        "dlux.Collection",
        on_delete=PROTECT,
        related_name="works",
    ),
    csv=["Parent ARK"],
    solr=[
        # TODO add a hook so we can look up titles, create ursus IDs
        "dlcs_collection_name_tesim",
        "member_of_collection_ids_ssim",
        "member_of_collections_ssim",
    ],
)

parent = DluxField(
    django=ForeignKey(
        "dlux.Work",
        on_delete=CASCADE,
        related_name="child_works",
    ),
    csv=["Parent ARK"],
    solr=[],
)

# there's probably a library out there that we should be using
order = DluxField(
    django=IntegerField(),
    csv=[],
    solr=[],
)

# should be required for Collection and Work records, maybe optional for ChildWorks?
title = DluxField(
    django=CharField(blank=False, max_length=250),
    csv=["Title"],
    solr=["title_tesim", "title_sim", "sort_title_tsort", "sort_title_ssort"],
)

description = DluxField(
    django=ArrayField(TextField(), blank=True),
    csv=["Description.note"],
    solr=["description_tesim"],
)

# TODO: this should be multivalued, but the standard django Arrayfield can't handle 'choices'.
# this is for demonstration; change to a django_jsonform Arrayfield for the final widget
resource_type = DluxField(
    # ArrayField(
    django=CharField(
        blank=False,
        choices=[
            ("http://id.loc.gov/vocabulary/resourceTypes/car", "cartographic"),
            ("http://id.loc.gov/vocabulary/resourceTypes/col", "collection"),
            ("http://id.loc.gov/vocabulary/resourceTypes/mix", "mixed material"),
            ("http://id.loc.gov/vocabulary/resourceTypes/mov", "moving image"),
            ("http://id.loc.gov/vocabulary/resourceTypes/not", "notated music"),
            ("http://id.loc.gov/vocabulary/resourceTypes/aud", "sound recording"),
            ("http://id.loc.gov/vocabulary/resourceTypes/aum", "sound recording-musical"),
            (
                "http://id.loc.gov/vocabulary/resourceTypes/aun",
                "sound recording-nonmusical",
            ),
            ("http://id.loc.gov/vocabulary/resourceTypes/img", "still image"),
            ("http://id.loc.gov/vocabulary/resourceTypes/txt", "text"),
            ("http://id.loc.gov/vocabulary/resourceTypes/art", "three dimensional object"),
        ],
        max_length=250,
    ),
    # ),
    csv=["Type.typeOfResource"],
    solr=[
        "human_readable_resource_type_tesim",
        "human_readable_resource_type_sim",
        "resource_type_sim",
        "resource_type_ssim",
        "resource_type_tesim",
    ],
)
