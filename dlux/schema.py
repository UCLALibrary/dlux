"""
Standard .

Uses a class-based syntax for readability and similarity to Django abstract classes, but is
equivalent to `TypedDict[str, DluxField]`.

Example:
>>> from django.db.models import CharField, IntegerField, Model

>>> from dlux.fields import DluxField, FieldGroup, with_field_groups


>>> class CharacterMetadata(FieldGroup):
>>>     name = DluxField(
>>>         django = CharField(max_length=200),
>>>         csv = ["Name"],
>>>         solr = ["name_tesi"],
>>>     )

>>> class MinionMetadata(FieldGroup):
>>>     n_eyes = DluxField(
>>>         django = IntegerField(),
>>>         csv = ["Eyes"],
>>>         solr = ["eyes_isi"],
>>>     )

>>> @with_field_groups(CharacterMetadata, MinionMetadata)
>>> class Minion(Model):
>>>     # Don't need this in practice, only here since we're not in models.py
>>>     class Meta:
>>>         app_label="dlux"

>>> james = Minion(name="James", n_eyes=1)
>>> james.name
"James"

>>> james.n_eyes
1

>>> james._meta.get_fields()
(<django.db.models.fields.BigAutoField: id>, <django.db.models.fields.CharField: name>,
<django.db.models.fields.IntegerField: n_eyes>)
"""

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

    resource_type = DluxField(
        django=ArrayField(
            models.CharField(
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


@with_field_groups(RequiredFields, UnsortedFieldsGroup)
class Collection(models.Model):
    pass


@with_field_groups(RequiredFields, BaseWork, UnsortedFieldsGroup)
class Work(models.Model):
    pass


@with_field_groups(RequiredFields, BaseChildWork, UnsortedFieldsGroup)
class ChildWork(models.Model):
    pass
