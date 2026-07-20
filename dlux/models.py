# pyright: reportCallIssue=false

from django.db import models
from django.db.models import ForeignKey

from dlux.fields import DluxExtra, MappedCharField, MappedForeignKey


class UniversalMetadata(models.Model):
    class Meta:
        abstract = True

    ark = MappedCharField(
        blank=False,
        dlux_extra=DluxExtra(
            csv=["Item ARK"],
            solr=["ark_ssi"],
        ),
    )


class UnsortedMetadata(models.Model):
    """
    Generic model that can take any of the fields we use. To gradually replace with models
    specific to different resource types
    """

    class Meta:
        abstract = True

    title = MappedCharField(
        blank=False,
        dlux_extra=DluxExtra(
            csv=["Title"],
            solr=["title_tesim", "title_sim", "sort_title_tsort", "sort_title_ssort"],
        ),
    )

    description = MappedCharField(
        blank=True,
        dlux_extra=DluxExtra(
            csv=["Description.note"],
            solr=["description_tesim"],
        ),
    )

    resource_type = MappedCharField(
        blank=False,
        choices=[
            (
                "http://id.loc.gov/vocabulary/resourceTypes/car",
                "cartographic",
            ),
            (
                "http://id.loc.gov/vocabulary/resourceTypes/col",
                "collection",
            ),
            (
                "http://id.loc.gov/vocabulary/resourceTypes/mix",
                "mixed material",
            ),
            (
                "http://id.loc.gov/vocabulary/resourceTypes/mov",
                "moving image",
            ),
            (
                "http://id.loc.gov/vocabulary/resourceTypes/not",
                "notated music",
            ),
            (
                "http://id.loc.gov/vocabulary/resourceTypes/aud",
                "sound recording",
            ),
            (
                "http://id.loc.gov/vocabulary/resourceTypes/aum",
                "sound recording-musical",
            ),
            (
                "http://id.loc.gov/vocabulary/resourceTypes/aun",
                "sound recording-nonmusical",
            ),
            (
                "http://id.loc.gov/vocabulary/resourceTypes/img",
                "still image",
            ),
            (
                "http://id.loc.gov/vocabulary/resourceTypes/txt",
                "text",
            ),
            (
                "http://id.loc.gov/vocabulary/resourceTypes/art",
                "three dimensional object",
            ),
        ],
        dlux_extra=DluxExtra(
            csv=["Type.typeOfResource"],
            solr=[
                "human_readable_resource_type_tesim",
                "human_readable_resource_type_sim",
                "resource_type_sim",
                "resource_type_ssim",
                "resource_type_tesim",
            ],
        ),
    )

    def __str__(self) -> str:
        return self.title  # pyright: ignore[reportUnknownVariableType, reportUnknownMemberType]


class Collection(  # pyright: ignore[reportIncompatibleVariableOverride]
    UniversalMetadata,
    UnsortedMetadata,
):
    pass


class Work(  # pyright: ignore[reportIncompatibleVariableOverride]
    UniversalMetadata,
    UnsortedMetadata,
):
    collection: "ForeignKey[Collection]" = MappedForeignKey(  # pyright: ignore[reportUnknownVariableType]
        Collection,
        on_delete=models.PROTECT,
    )
