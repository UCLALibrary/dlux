from django.contrib.postgres.fields import ArrayField
from django.db import models

from dlux.fields import DluxField, FieldGroup, with_field_groups


class RequiredFields(FieldGroup):
    ark = DluxField(
        django=models.CharField(unique=True, blank=False, max_length=2000),
        csv=["Item ARK"],
        solr=["ark_ssi"],
    )


class BaseWork(FieldGroup):
    collection = DluxField(
        django=models.ForeignKey(
            "dlux.Collection",
            on_delete=models.PROTECT,
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


class BaseChildWork(FieldGroup):
    _constraints = [models.UniqueConstraint(fields=["parent", "order"], name="unique_parent_order")]

    parent = DluxField(
        django=models.ForeignKey(
            "dlux.Work",
            on_delete=models.CASCADE,
            related_name="child_works",
        ),
        csv=["Parent ARK"],
        solr=[],
    )

    order = DluxField(
        django=models.IntegerField(),
        csv=[],
        solr=[],
    )


class UnsortedFieldsGroup(FieldGroup):
    title = DluxField(
        django=models.CharField(blank=False, max_length=250),
        csv=["Title"],
        solr=["title_tesim", "title_sim", "sort_title_tsort", "sort_title_ssort"],
    )

    description = DluxField(
        django=ArrayField(models.TextField(), blank=True),
        csv=["Description.note"],
        solr=["description_tesim"],
    )

    # TODO: this should be multivalued, but the standard django Arrayfield can't handle 'choices'.
    # this is for demonstration; change to a django_jsonform Arrayfield for the final widget

    resource_type = DluxField(
        # ArrayField(
        django=models.CharField(
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


@with_field_groups(RequiredFields, UnsortedFieldsGroup)
class Collection(models.Model):
    title: "models.CharField[str]"

    def __str__(self) -> str:
        return self.title


@with_field_groups(RequiredFields, BaseWork, UnsortedFieldsGroup)
class Work(models.Model):
    title: "models.CharField[str]"

    def __str__(self) -> str:
        return self.title


@with_field_groups(RequiredFields, BaseChildWork, UnsortedFieldsGroup)
class ChildWork(models.Model):
    title: "models.CharField[str]"

    def __str__(self) -> str:
        return self.title
