"""Django models for dlux.

Our data model is defined in dlux-specific FieldGroup and DluxField objects, which should probably
be moved outside the standard django file structure. Django models are then created programmatically
from those objects.
"""

from django.db.models import (
    CASCADE,
    PROTECT,
    CharField,
    ForeignKey,
    IntegerField,
    TextField,
)

from dlux.fields import ArrayField, DluxField

ark = DluxField(
    django=CharField(unique=True),
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

title = DluxField(
    django=CharField(),
    csv=["Title"],
    solr=["title_tesim", "title_sim", "sort_title_tsort", "sort_title_ssort"],
)

description = DluxField(
    django=ArrayField(TextField(), blank=True),
    csv=["Description.note"],
    solr=["description_tesim"],
)

resource_type = DluxField(
    django=ArrayField(
        CharField(
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
        ),
        blank=True,
        default=list,
    ),
    csv=["Type.typeOfResource"],
    solr=[
        "human_readable_resource_type_tesim",
        "human_readable_resource_type_sim",
        "resource_type_sim",
        "resource_type_ssim",
        "resource_type_tesim",
    ],
)
