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


class DateInfoFields(PolymorphicModel):
    """Date-related fields for all dlux record types."""

    class Meta(PolymorphicModel.Meta):
        """Django model Meta options.

        see:
        https://docs.djangoproject.com/en/5.2/ref/models/options/
        """

        abstract = True

    date_created = dlux_fields.date_created.django
    normalized_date = dlux_fields.normalized_date.django


class DigitalAssetFields(PolymorphicModel):
    """Digital asset fields for all dlux record types."""

    class Meta(PolymorphicModel.Meta):
        """Django model Meta options.

        see:
        https://docs.djangoproject.com/en/5.2/ref/models/options/
        """

        abstract = True

    access_copy = dlux_fields.access_copy.django
    iiif_manifest_url = dlux_fields.iiif_manifest_url.django
    iiif_viewing_hint = dlux_fields.iiif_viewing_hint.django
    preservation_copy = dlux_fields.preservation_copy.django
    thumbnail_url = dlux_fields.thumbnail_url.django


class LibraryInfoFields(PolymorphicModel):
    """Library-related fields for all dlux record types."""

    class Meta(PolymorphicModel.Meta):
        """Django model Meta options.

        see:
        https://docs.djangoproject.com/en/5.2/ref/models/options/
        """

        abstract = True

    archival_collection_box = dlux_fields.archival_collection_box.django
    archival_collection_folder = dlux_fields.archival_collection_folder.django
    archival_collection_number = dlux_fields.archival_collection_number.django
    archival_collection_title = dlux_fields.archival_collection_title.django
    finding_aid_url = dlux_fields.finding_aid_url.django
    funding_note = dlux_fields.funding_note.django
    local_identifier = dlux_fields.local_identifier.django
    local_rights_statement = dlux_fields.local_rights_statement.django
    opac_url = dlux_fields.opac_url.django
    program = dlux_fields.program.django
    repository = dlux_fields.repository.django
    rights_country = dlux_fields.rights_country.django
    rights_statement = dlux_fields.rights_statement.django
    services_contact = dlux_fields.services_contact.django


class PhysicalMediaFields(PolymorphicModel):
    """Physical media fields for all dlux record types."""

    class Meta(PolymorphicModel.Meta):
        """Django model Meta options.

        see:
        https://docs.djangoproject.com/en/5.2/ref/models/options/
        """

        abstract = True

    binding_condition = dlux_fields.binding_condition.django
    binding_note = dlux_fields.binding_note.django
    collation = dlux_fields.collation.django
    condition_note = dlux_fields.condition_note.django
    dimensions = dlux_fields.dimensions.django
    extent = dlux_fields.extent.django
    folio_dimensions = dlux_fields.folio_dimensions.django
    form = dlux_fields.form.django
    format_book = dlux_fields.format_book.django
    medium = dlux_fields.medium.django
    page_layout = dlux_fields.page_layout.django
    shelfmark = dlux_fields.shelfmark.django

    @property
    def condition_note_ssi(self) -> str | None:
        """Return the first condition note value for SSI indexing."""
        return (
            self.condition_note[0]
            if (self.condition_note and len(self.condition_note) >= 1)
            else None
        )

    # TODO is this property necessary?
    @property
    def binding_note_tesim(self) -> list[str] | None:
        """Return the binding note as a list for TESIM indexing."""
        return [self.binding_note] if self.binding_note else None


class GeographicFields(PolymorphicModel):
    """Geographic data fields for all dlux record types."""

    class Meta(PolymorphicModel.Meta):
        """Django model Meta options.

        see:
        https://docs.djangoproject.com/en/5.2/ref/models/options/
        """

        abstract = True

    latitude = dlux_fields.latitude.django
    location = dlux_fields.location.django
    longitude = dlux_fields.longitude.django
    subject_geographic = dlux_fields.subject_geographic.django

    # TODO: Properties like this do not currently display in admin UI. Should they?
    @property
    def geographic_coordinates_ssim(self) -> list[str] | None:
        """Return latitude and longitude pairs formatted for SSIM indexing."""
        return [
            ", ".join([lat, long])
            for lat, long in zip(
                self.latitude or [],
                self.longitude or [],
            )
        ] or None

    def longitudes_match_latitudes(self) -> None:
        """Verify that latitude and longitude pairs are properly matched."""
        if len(self.latitude or []) != len(self.longitude or []):
            raise ValueError(
                "\n".join(
                    [
                        "Mismatched lengths:",
                        f"Latitude {self.latitude}",
                        f"Longitude {self.longitude}",
                    ]
                )
            )


class ExtraDescriptiveFields(PolymorphicModel):
    """Extra descriptive fields for all dlux record types."""

    class Meta(PolymorphicModel.Meta):
        """Django model Meta options.

        see:
        https://docs.djangoproject.com/en/5.2/ref/models/options/
        """

        abstract = True

    alternative_title = dlux_fields.alternative_title.django
    architect = dlux_fields.architect.django
    arranger = dlux_fields.arranger.django
    artist = dlux_fields.artist.django
    associated_name = dlux_fields.associated_name.django
    author = dlux_fields.author.django
    calligrapher = dlux_fields.calligrapher.django
    cartographer = dlux_fields.cartographer.django
    collector = dlux_fields.collector.django
    colophon = dlux_fields.colophon.django
    commentator = dlux_fields.commentator.django
    composer = dlux_fields.composer.django
    contributor = dlux_fields.contributor.django
    descriptive_title = dlux_fields.descriptive_title.django
    director = dlux_fields.director.django
    edition = dlux_fields.edition.django
    editor = dlux_fields.editor.django
    engraver = dlux_fields.engraver.django
    illuminator = dlux_fields.illuminator.django
    illustrator = dlux_fields.illustrator.django
    interviewee = dlux_fields.interviewee.django
    interviewer = dlux_fields.interviewer.django
    librettist = dlux_fields.librettist.django
    lyricist = dlux_fields.lyricist.django
    musician = dlux_fields.musician.django
    named_subject = dlux_fields.named_subject.django
    place_of_origin = dlux_fields.place_of_origin.django
    printer = dlux_fields.printer.django
    printmaker = dlux_fields.printmaker.django
    producer = dlux_fields.producer.django
    provenance = dlux_fields.provenance.django
    recipient = dlux_fields.recipient.django
    researcher = dlux_fields.researcher.django
    rights_holder = dlux_fields.rights_holder.django
    rubricator = dlux_fields.rubricator.django
    scribe = dlux_fields.scribe.django
    script = dlux_fields.script.django
    script_note = dlux_fields.script_note.django
    series = dlux_fields.series.django
    subject_cultural_object = dlux_fields.subject_cultural_object.django
    subject_domain_topic = dlux_fields.subject_domain_topic.django
    subject_temporal = dlux_fields.subject_temporal.django
    summary = dlux_fields.summary.django
    table_of_contents = dlux_fields.table_of_contents.django
    translator = dlux_fields.translator.django
    uniform_title = dlux_fields.uniform_title.django
    writing_system = dlux_fields.writing_system.django


class UnsortedFields(PolymorphicModel):
    """Remaining fields to be categorized later, for all dlux record types."""

    class Meta(PolymorphicModel.Meta):
        """Django model Meta options.

        see:
        https://docs.djangoproject.com/en/5.2/ref/models/options/
        """

        abstract = True

    citation_source = dlux_fields.citation_source.django
    content_disclaimer = dlux_fields.content_disclaimer.django
    contents_note = dlux_fields.contents_note.django
    contents = dlux_fields.contents.django
    delivery = dlux_fields.delivery.django
    electronic_locator = dlux_fields.electronic_locator.django
    explicit = dlux_fields.explicit.django
    featured_image = dlux_fields.featured_image.django
    features = dlux_fields.features.django
    foliation = dlux_fields.foliation.django
    hand_note = dlux_fields.hand_note.django
    history = dlux_fields.history.django
    host = dlux_fields.host.django
    identifier = dlux_fields.identifier.django
    iiif_range = dlux_fields.iiif_range.django
    iiif_text_direction = dlux_fields.iiif_text_direction.django
    illustrations_note = dlux_fields.illustrations_note.django
    image_count = dlux_fields.image_count.django
    incipit = dlux_fields.incipit.django
    license = dlux_fields.license.django
    masthead_parameters = dlux_fields.masthead_parameters.django
    note_admin = dlux_fields.note_admin.django
    note = dlux_fields.note.django
    oai_set = dlux_fields.oai_set.django
    other_versions = dlux_fields.other_versions.django
    related_record = dlux_fields.related_record.django
    related_to = dlux_fields.related_to.django
    representative_image = dlux_fields.representative_image.django
    resp_statement = dlux_fields.resp_statement.django
    support = dlux_fields.support.django
    tagline = dlux_fields.tagline.django
    visibility = dlux_fields.visibility.django


#
#   A single concrete model to represent all our data in the db.
#


class Record(
    BasicDescriptiveFields,
    DateInfoFields,
    DigitalAssetFields,
    GeographicFields,
    LibraryInfoFields,
    PhysicalMediaFields,
    ExtraDescriptiveFields,
    UnsortedFields,
):
    """A dlux record.

    The underlying model that represents all data types in a single database table. Should not be
    used directly; most actual interactions should use the proxy models defined below.

    More on proxy models in the django core:
    https://docs.djangoproject.com/en/5.2/topics/db/models/#proxy-models

    django-polymorphic, which makes working with proxy models easier:
    https://django-polymorphic.readthedocs.io/en/stable/

    The django-polymorphic docs are mostly written assuming one is using multi-table inheritance,
    but it also supports proxy models without significant differences in developer interface.

    In particular, django-polymorphic creates a field in the database to represent the proxy model
    associated with a given record, so a search for `Record` objects can return individual
    `Collection`, `Work`, and `ChildWork` objects.
    """

    ark = dlux_fields.ark.django
    title = dlux_fields.title.django
    parent = dlux_fields.parent.django
    sequence = dlux_fields.sequence.django

    class Meta(
        BasicDescriptiveFields.Meta,
        DateInfoFields.Meta,
        DigitalAssetFields.Meta,
        GeographicFields.Meta,
        LibraryInfoFields.Meta,
        PhysicalMediaFields.Meta,
        ExtraDescriptiveFields.Meta,
        UnsortedFields.Meta,
    ):
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
        proxy = False  # The default, just being explicit

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
