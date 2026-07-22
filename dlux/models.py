"""Django models for dlux.

Our data model is defined in dlux-specific FieldGroup and DluxField objects, which should probably
be moved outside the standard django file structure. Django models are then created programmatically
from those objects.
"""

from django.db.models import Model, UniqueConstraint

from dlux import dlux_fields

#
#   Abstract models define bundles of related fields
#


class BaseDluxRecord(Model):
    """Base model for all dlux record types.

    Contains universally-required fields and utilities for dlux record models
    """

    class Meta:
        """Django model Meta options.

        see:
        https://docs.djangoproject.com/en/5.2/ref/models/options/
        """

        abstract = True
        constraints = [
            UniqueConstraint(fields=["ark"], name="%(app_label)s_%(class)s_test_constraint")
        ]

    ark = dlux_fields.ark.django

    @classmethod
    def get_dlux_fields(cls, include_parents: bool = True) -> list[dlux_fields.DluxField]:
        """Return the original DluxField objects for a record's fields."""
        return [
            getattr(dlux_fields, field.name)
            for field in cls._meta.get_fields(include_parents=include_parents)
            if isinstance(getattr(dlux_fields, field.name, None), dlux_fields.DluxField)
        ]


class UnsortedFields(Model):
    """'Kitchen-Sink' style FieldGroup for fields we haven't sorted yet."""

    class Meta:
        """Django model Meta options.

        see:
        https://docs.djangoproject.com/en/5.2/ref/models/options/
        """

        abstract = True

    # move this? should be required for Collection and Work records, maybe optional for ChildWorks?
    title = dlux_fields.title.django
    description = dlux_fields.description.django
    resource_type = dlux_fields.resource_type.django


#
#   Concerete Models
#


class Collection(BaseDluxRecord, UnsortedFields):
    """A dlux collection.

    Record is displayed publicly at https://digital.library.ucla.edu/catalog?f%5Bhas_model_ssim%5D%5B%5D=Collection&view=list

    A dlux Collection is parent to a number of member Works.
    """

    class Meta(BaseDluxRecord.Meta, UnsortedFields.Meta):
        """Django model Meta options.

        see:
        https://docs.djangoproject.com/en/5.2/ref/models/options/

        Included here because including the parent Meta classes silences a type error.
        """

        pass

    def __str__(self) -> str:
        """Return the record title as a user-friendly representation of the object."""
        return self.title


class Work(BaseDluxRecord, UnsortedFields):
    """A dlux work.

    Record is displayed publicly at https://digital.library.ucla.edu/catalog?utf8=✓&view=list&f%5Bhas_model_ssim%5D%5B%5D=Collection&q=&search_field=all_fields

    A dlux Work is a member of a collection and can optionally be parent to a number of ChildWorks.
    """

    class Meta(BaseDluxRecord.Meta, UnsortedFields.Meta):
        """Django model Meta options.

        see:
        https://docs.djangoproject.com/en/5.2/ref/models/options/

        Included here to silence a type error.
        """

        pass

    collection = dlux_fields.collection.django

    def __str__(self) -> str:
        """Return the record title as a user-friendly representation of the object."""
        return self.title


class ChildWork(BaseDluxRecord, UnsortedFields):
    """A dlux child work: for example a page in a Manuscript.

    Record is not intended to be displayed publicly via its own item page on https://digital.library.ucla.edu
    (A few old records might currently have accessible item pages, but this is not intended and they
    are never included in search results.)

    The data is used in the creation of iiif manifests (see https://github.com/uclalibrary/fester),
    through which they can be browsed in the viewer section of the parent work.

    A dlux ChildWork must be the child of a Work.
    """

    class Meta(BaseDluxRecord.Meta, UnsortedFields.Meta):
        """Django model Meta options.

        see:
        https://docs.djangoproject.com/en/5.2/ref/models/options/
        """

        constraints = [
            UniqueConstraint(
                fields=["parent", "order"],
                name="childwork_unique_order_per_parent",
            )
        ]

    parent = dlux_fields.parent.django
    order = dlux_fields.order.django

    def __str__(self) -> str:
        """Return a user-friendly representation of the object.

        Representation includes parent record's title, the order within parent record, and the
        record's own title.
        """
        # type annotations get tricky here, even with the manual annotations
        return f"{self.parent.title} ({self.order}): {self.title}"  # pyright: ignore[reportAttributeAccessIssue, reportUnknownMemberType]
