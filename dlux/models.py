"""Django models for dlux.

Our data model is defined in dlux-specific FieldGroup and DluxField objects, which should probably
be moved outside the standard django file structure. Django models are then created programmatically
from those objects.
"""

from typing import Literal, overload

from django.db.models import Model, UniqueConstraint
from polymorphic.models import PolymorphicModel

from dlux import dlux_fields
from dlux.fields import DluxField

#
#   Abstract models define bundles of related fields
#

DluxFieldsList = dict[str, DluxField]
DluxFieldsByBaseClass = dict[str, DluxFieldsList]


class BasicDescriptiveFields(PolymorphicModel):
    """Basic descriptive fields for all dlux record types."""

    class Meta(PolymorphicModel.Meta):
        """Django model Meta options.

        see:
        https://docs.djangoproject.com/en/5.2/ref/models/options/
        """

        abstract = True

    caption = dlux_fields.caption.django
    creator = dlux_fields.creator.django
    description = dlux_fields.description.django
    genre = dlux_fields.genre.django
    inscription = dlux_fields.inscription.django
    language = dlux_fields.language.django
    photographer = dlux_fields.photographer.django
    publisher = dlux_fields.publisher.django
    resource_type = dlux_fields.resource_type.django
    subject = dlux_fields.subject.django
    subject_topic = dlux_fields.subject_topic.django


#
#   A single concrete model to represent all our data in the db.
#


class Record(BasicDescriptiveFields):
    """A dlux record.

    The underlying model that represents all data types in a single database table. Should not be
    used directly; most actual interactions should use the proxy models defined below.
    """

    ark = dlux_fields.ark.django
    title = dlux_fields.title.django
    parent = dlux_fields.parent.django
    sequence = dlux_fields.sequence.django

    class Meta(BasicDescriptiveFields.Meta):
        """Django model Meta options.

        see:
        https://docs.djangoproject.com/en/5.2/ref/models/options/
        """

        constraints = [
            UniqueConstraint(
                fields=["parent", "sequence"],
                name="childwork_unique_sequence_per_parent",
                nulls_distinct=True,
            )
        ]

    def __str__(self) -> str:
        """Return the record title as a user-friendly representation of the object."""
        return self.title

    @overload
    @classmethod
    def get_dlux_fields(cls, by_base_class: Literal[False]) -> DluxFieldsList: ...

    @overload
    @classmethod
    def get_dlux_fields(cls, by_base_class: Literal[True]) -> DluxFieldsByBaseClass: ...

    @classmethod
    def get_dlux_fields(
        cls,
        by_base_class: bool = False,
    ) -> DluxFieldsList | DluxFieldsByBaseClass:
        """Return the original DluxField objects for a record's fields.

        Differs from the built-in Model._meta.get_fields() in that it returns DluxField objects,
        where we have included addition information about the field relevant to dlux, rather than
        Django Field instances.

        Args:
            by_base_class: A boolean flag determining the output format. If true, fields are
            grouped according to the underlying abstract classes in which they are defined.
            (See "Returns".)

        Returns:
            If by_base_class==False, returns a dict mapping field names to DluxField objects:
                model_name: {
                    field_name: dlux_field,
                    ...,
                },

            If by_base_class==True, returns a dict mapping the names of abstract models to dicts
            describing the fields defined in those models. Each inner dict has the same form as the
            output if by_base_class is False, but contains only the fields inherited from that
            model:
                {
                    model_name: {
                        field_name: dlux_field,
                        ...,
                    },
                    ...
                }
        """
        all_fields: DluxFieldsList = {}
        for field in cls._meta.get_fields():
            dlux_field = getattr(dlux_fields, field.name, None)
            if isinstance(dlux_field, dlux_fields.DluxField) and not issubclass(
                cls, dlux_field.get_exclude_models()
            ):
                all_fields[field.name] = dlux_field

        if by_base_class:
            result: DluxFieldsByBaseClass = {"Record": all_fields}

            for subcls in Record.__bases__:
                if issubclass(subcls, Model) and subcls.__name__:
                    result[subcls.__name__] = {
                        field.name: result["Record"].pop(field.name)
                        for field in subcls._meta.get_fields()
                        if field.name in result["Record"]
                    }

            return result

        else:
            return all_fields


#
#   Type-specific proxy models to interact with the data.
#


class Collection(Record):
    """A dlux collection.

    Record is displayed publicly at https://digital.library.ucla.edu/catalog?f%5Bhas_model_ssim%5D%5B%5D=Collection&view=list

    A dlux Collection is parent to a number of member Works.
    """

    class Meta(Record.Meta):
        """Django model Meta options.

        see:
        https://docs.djangoproject.com/en/5.2/ref/models/options/
        """

        proxy = True


class Work(Record):
    """A dlux work.

    Record is displayed publicly at https://digital.library.ucla.edu/catalog?utf8=✓&view=list&f%5Bhas_model_ssim%5D%5B%5D=Collection&q=&search_field=all_fields

    A dlux Work is a member of a collection and can optionally be parent to a number of ChildWorks.
    """

    class Meta(Record.Meta):
        """Django model Meta options.

        see:
        https://docs.djangoproject.com/en/5.2/ref/models/options/
        """

        proxy = True


class ChildWork(Record):
    """A dlux child work: for example a page in a Manuscript.

    Record is not intended to be displayed publicly via its own item page on https://digital.library.ucla.edu
    (A few old records might currently have accessible item pages, but this is not intended and they
    are never included in search results.)

    The data is used in the creation of iiif manifests (see https://github.com/uclalibrary/fester),
    through which they can be browsed in the viewer section of the parent work.

    A dlux ChildWork must be the child of a Work.
    """

    class Meta(Record.Meta):
        """Django model Meta options.

        see:
        https://docs.djangoproject.com/en/5.2/ref/models/options/
        """

        proxy = True
