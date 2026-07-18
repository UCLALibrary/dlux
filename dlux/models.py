"""Django models for dlux.

Our data model is defined in dlux-specific FieldGroup and DluxField objects, which should probably
be moved outside the standard django file structure. Django models are then created programmatically
from those objects.
"""

from django.contrib.postgres.fields import ArrayField
from django.db import models

from dlux.fields import DluxField, FieldGroup, with_field_groups

#
#   FieldGroups to define data model (move to another file?)
#


class RequiredFields(FieldGroup):
    """Required fields for all dlux records."""

    ark = DluxField(
        django=models.CharField(unique=True, blank=False, max_length=2000),
        csv=["Item ARK"],
        solr=["ark_ssi"],
    )


class BaseWork(FieldGroup):
    """Base fields to include in any "work-level" record.

    Defines membership in a collection.
    """

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
    """Base fields for "child-work-level" records.

    Records defined as ordered children of a particular parent work.
    """

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

    # there's probably a library out there that we should be using
    order = DluxField(
        django=models.IntegerField(),
        csv=[],
        solr=[],
    )


class UnsortedFieldsGroup(FieldGroup):
    """'Kitchen-Sink' style FieldGroup for fields we haven't sorted yet."""

    # move this? should be required for Collection and Work records, maybe optional for ChildWorks?
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


#
#   Django Models
#


@with_field_groups(RequiredFields, UnsortedFieldsGroup)
class Collection(models.Model):
    """A dlux collection.

    Record is displayed publicly at https://digital.library.ucla.edu/catalog?f%5Bhas_model_ssim%5D%5B%5D=Collection&view=list

    A dlux Collection is parent to a number of member Works.
    """

    # manually annotate, since fields added via with_field_groups() are invisible to type checker.
    title: "models.CharField[str]"

    def __str__(self) -> str:
        """Return the record title as a user-friendly representation of the object."""
        return self.title


@with_field_groups(RequiredFields, BaseWork, UnsortedFieldsGroup)
class Work(models.Model):
    """A dlux work.

    Record is displayed publicly at https://digital.library.ucla.edu/catalog?utf8=✓&view=list&f%5Bhas_model_ssim%5D%5B%5D=Collection&q=&search_field=all_fields

    A dlux Work is a member of a collection and can optionally be parent to a number of ChildWorks.
    """

    # manually annotate, since fields added via with_field_groups() are invisible to type checker.
    title: "models.CharField[str]"

    def __str__(self) -> str:
        """Return the record title as a user-friendly representation of the object."""
        return self.title


@with_field_groups(RequiredFields, BaseChildWork, UnsortedFieldsGroup)
class ChildWork(models.Model):
    """A dlux child work: for example a page in a Manuscript.

    Record is not intended to be displayed publicly via its own item page on https://digital.library.ucla.edu
    (A few old records might currently have accessible item pages, but this is not intended and they
    are never included in search results.)

    The data is used in the creation of iiif manifests (see https://github.com/uclalibrary/fester),
    through which they can be browsed in the viewer section of the parent work.

    A dlux ChildWork must be the child of a Work.
    """

    # manually annotate, since fields added via with_field_groups() are invisible to type checker.

    title: "models.CharField[str]"  # not optional now, but maybe should be?
    parent: "models.ForeignKey[Work]"
    order: "models.IntegerField[int]"

    def __str__(self) -> str:
        """Return a user-friendly representation of the object.

        Representation includes parent record's title, the order within parent record, and the
        record's own title.
        """
        # type annotations get tricky here, even with the manual annotations
        return f"{self.parent.title} ({self.order}): {self.title}"  # pyright: ignore[reportAttributeAccessIssue, reportUnknownMemberType]
