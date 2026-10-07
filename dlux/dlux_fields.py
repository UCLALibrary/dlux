"""Django models for dlux.

Our data model is defined in dlux-specific FieldGroup and DluxField objects, which should probably
be moved outside the standard django file structure. Django models are then created programmatically
from those objects.
"""

from typing import TYPE_CHECKING

from django.core.validators import RegexValidator
from django.db.models import (
    PROTECT,
    CharField,
    ForeignKey,
    IntegerField,
    TextField,
)

from dlux.choices import (
    IIIF_TEXT_DIRECTION_CHOICES,
    IIIF_VIEWING_HINT_CHOICES,
    LANGUAGE_CHOICES,
    RESOURCE_TYPE_CHOICES,
    RIGHTS_STATEMENT_CHOICES,
    VISIBILITY_CHOICES,
)
from dlux.fields import ArrayField, DluxField

if TYPE_CHECKING:
    from django_jsonform.models.fields import ArraySchema

# Used to set widget rendered in admin forms to textarea
# for longer textual fields wrapped in ArrayField
TEXTAREA_ARRAY_SCHEMA: "ArraySchema" = {
    "type": "list",
    "items": {
        "type": "string",
        "widget": "textarea",
    },
}

# Used to validate `normalized_date`.
# DATE_PATTERN matches YYYY, YYYY-MM, or YYYY-MM-DD,
# with optional negative sign and 3+ digits for year.
# NORMALIZED_DATE_REGEX then matches a DATE_PATTERN,
# optionally followed by a slash and another DATE_PATTERN for ranges.
DATE_PATTERN = r"-?\d?\d\d\d(-\d\d){0,2}"
NORMALIZED_DATE_REGEX = rf"^{DATE_PATTERN}(/{DATE_PATTERN})?$"

# Used to validate `preservation_copy`.
# Matches path-like strings with particular folder structure,
# e.g. "Masters/dlmasters/filename.tif" or "Masters/othermasters/filename.jpg".
PRESERVATION_COPY_REGEX = r"^Masters/(dlmasters|CDLIMasters|Livingstone|Maps|MEAP|othermasters)/.+"


#
#   NOTE
#
#   The order in which fields appear in the admin panels is determined by the order in which the
#   Field objects are first created, which for dlux is the order they are defined in this file, NOT
#   the order in which they are added in models.py.
#


#
#   Top fields: in the order we want them to appear.
#

title = DluxField(
    django=CharField(),
    csv=["Title"],
    solr=["title_tesim", "title_sim", "sort_title_tsort", "sort_title_ssort"],
)

ark = DluxField(
    django=CharField(unique=True),
    csv=["Item ARK"],
    solr=["ark_ssi"],
)

# polymorphic_ctype gets created automatically by django-polymorphic to keep track of which proxy
# model a record belongs to. We should not add it to the models manually. Not sure the best way to
# handle it for import and indexing (AW 8/19/26); so leaving this commented out as a marker.

# polymorphic_ctype = DluxField(
#     django=ForeignKey(ContentType, on_delete=PROTECT),
#     csv=["Object Type"],
#     solr=["has_model_ssim"],
# )


parent = DluxField(
    django=ForeignKey(
        "dlux.Record",
        blank=True,
        null=True,
        on_delete=PROTECT,
        related_name="children",
    ),
    csv=["Parent ARK"],
    solr=[],
    exclude_models=["Collection"],
)

# there's probably a library out there that we should be using
sequence = DluxField(
    django=IntegerField(blank=True, null=True),
    csv=["Item Sequence"],
    solr=[],
    exclude_models=["Collection", "Work"],
)


#
#   Other fields: keep these alphabetized
#
access_copy = DluxField(
    django=CharField(blank=True),
    csv=[
        "access_copy",
        "IIIF Access URL",
    ],
    solr=["access_copy_ssi"],
)

alternative_title = DluxField(
    django=ArrayField(
        TextField(),
        blank=True,
        default=list,
    ),
    csv=[
        "AltTitle.other",
        "AltTitle.parallel",
        "AltTitle.translated",
        "Alternate Title.creator",
        "Alternate Title.descriptive",
        "Alternate Title.inscribed",
        "AltTitle.descriptive",
        "Alternate Title.other",
    ],
    solr=["alternative_title_tesim"],
)

architect = DluxField(
    django=ArrayField(
        TextField(),
        blank=True,
        default=list,
    ),
    csv=["Name.architect"],
    solr=["architect_tesim", "architect_sim"],
)

archival_collection_box = DluxField(
    django=CharField(blank=True),
    csv=["Box"],
    solr=["archival_collection_box_ssi"],
)

archival_collection_folder = DluxField(
    django=CharField(blank=True),
    csv=["Folder"],
    solr=["archival_collection_folder_ssi"],
)

archival_collection_number = DluxField(
    django=CharField(blank=True),
    csv=["Archival Collection Number"],
    solr=["archival_collection_number_ssi"],
)

archival_collection_title = DluxField(
    django=CharField(blank=True),
    csv=["Archival Collection Title"],
    solr=["archival_collection_title_ssi"],
)

arranger = DluxField(
    django=ArrayField(
        TextField(),
        blank=True,
        default=list,
    ),
    csv=["Arranger", "Name.arranger"],
    solr=["arranger_tesim", "arranger_sim"],
)

artist = DluxField(
    django=ArrayField(
        TextField(),
        blank=True,
        default=list,
    ),
    csv=["Artist", "Name.artist"],
    solr=["artist_tesim", "artist_sim"],
)

associated_name = DluxField(
    django=ArrayField(
        TextField(),
        blank=True,
        default=list,
    ),
    csv=["Associated Name"],
    solr=["associated_name_tesim", "associated_name_sim"],
)

author = DluxField(
    django=ArrayField(
        TextField(),
        blank=True,
        default=list,
    ),
    csv=["Author"],
    solr=["author_tesim", "author_sim"],
)

binding_condition = DluxField(
    django=ArrayField(
        TextField(),
        blank=True,
        default=list,
    ),
    csv=["Binding condition"],
    solr=["binding_condition_tesim"],
)

binding_note = DluxField(
    django=TextField(blank=True, default=""),
    csv=["Binding note", "Description.binding"],
    solr=["binding_note_tesim", "binding_note_ssi"],
)

calligrapher = DluxField(
    django=ArrayField(
        TextField(),
        blank=True,
        default=list,
    ),
    csv=["Calligrapher", "Name.calligrapher"],
    solr=["calligrapher_tesim", "calligrapher_sim"],
)

caption = DluxField(
    django=ArrayField(
        TextField(),
        blank=True,
        default=list,
        schema=TEXTAREA_ARRAY_SCHEMA,
    ),
    csv=["Description.caption"],
    solr=["caption_tesim"],
)

cartographer = DluxField(
    django=ArrayField(
        TextField(),
        blank=True,
        default=list,
    ),
    csv=["Cartographer", "Name.cartographer"],
    solr=["cartographer_tesim", "cartographer_sim"],
)

citation_source = DluxField(
    django=ArrayField(
        TextField(),
        blank=True,
        default=list,
    ),
    csv=["References"],
    solr=["citation_source_tesim"],
)

collation = DluxField(
    django=ArrayField(
        TextField(),
        blank=True,
        default=list,
    ),
    csv=["Collation"],
    solr=["collation_tesim"],
)

collector = DluxField(
    django=ArrayField(
        TextField(),
        blank=True,
        default=list,
    ),
    csv=["Collector"],
    solr=["collector_tesim", "collector_sim"],
)

colophon = DluxField(
    django=ArrayField(
        TextField(),
        blank=True,
        default=list,
        schema=TEXTAREA_ARRAY_SCHEMA,
    ),
    csv=["Colophon", "Description.colophon"],
    solr=["colophon_tesim"],
)

commentator = DluxField(
    django=ArrayField(
        TextField(),
        blank=True,
        default=list,
    ),
    csv=["Commentator", "Name.commentator"],
    solr=["commentator_tesim", "commentator_sim"],
)

composer = DluxField(
    django=ArrayField(
        TextField(),
        blank=True,
        default=list,
    ),
    csv=["Name.composer"],
    solr=["composer_tesim", "composer_sim"],
)

condition_note = DluxField(
    django=ArrayField(
        TextField(),
        blank=True,
        default=list,
    ),
    csv=["Condition note", "Description.condition"],
    solr=["condition_note_tesim"],
)

content_disclaimer = DluxField(
    django=ArrayField(
        TextField(),
        blank=True,
        default=list,
    ),
    csv=["Content disclaimer"],
    solr=["content_disclaimer_ssm"],
)

contents_note = DluxField(
    django=ArrayField(
        TextField(),
        blank=True,
        default=list,
    ),
    csv=["Contents note"],
    solr=["contents_note_tesim"],
)

contents = DluxField(
    django=ArrayField(
        TextField(),
        blank=True,
        default=list,
    ),
    csv=["Contents"],
    solr=["contents_tesim"],
)

contributor = DluxField(
    django=ArrayField(
        TextField(),
        blank=True,
        default=list,
    ),
    csv=["Contributors"],
    solr=["contributor_tesim"],
)

creator = DluxField(
    django=ArrayField(
        TextField(),
        blank=True,
        default=list,
    ),
    csv=["Creator", "Name.creator"],
    solr=["creator_tesim", "creator_sim"],
)

date_created = DluxField(
    django=ArrayField(TextField(), blank=True, default=list),
    csv=["Date.created", "Date.creation"],
    solr=["date_created_tesim"],
)

delivery = DluxField(
    django=ArrayField(
        TextField(),
        blank=True,
        default=list,
    ),
    csv=["delivery"],
    solr=["delivery_tesim"],
)

description = DluxField(
    django=ArrayField(
        TextField(),
        blank=True,
        default=list,
        schema=TEXTAREA_ARRAY_SCHEMA,
    ),
    csv=["Description.note"],
    solr=["description_tesim"],
)

descriptive_title = DluxField(
    django=ArrayField(
        TextField(),
        blank=True,
        default=list,
        schema=TEXTAREA_ARRAY_SCHEMA,
    ),
    csv=["Descriptive title"],
    solr=["descriptive_title_tesim"],
)

dimensions = DluxField(
    django=ArrayField(
        TextField(),
        blank=True,
        default=list,
    ),
    csv=["Format.dimensions"],
    solr=["dimensions_tesim", "dimensions_sim"],
)

director = DluxField(
    django=ArrayField(
        TextField(),
        blank=True,
        default=list,
    ),
    csv=["Director", "Name.director"],
    solr=["director_tesim", "director_sim"],
)

edition = DluxField(
    django=ArrayField(
        TextField(),
        blank=True,
        default=list,
    ),
    csv=["Edition"],
    solr=["edition_ssm"],
)

editor = DluxField(
    django=ArrayField(
        TextField(),
        blank=True,
        default=list,
    ),
    csv=["Editor", "Name.editor"],
    solr=["editor_tesim", "editor_sim"],
)

electronic_locator = DluxField(
    django=CharField(blank=True),
    csv=["External item record", "View Record"],
    solr=["electronic_locator_ss"],
)

engraver = DluxField(
    django=ArrayField(
        TextField(),
        blank=True,
        default=list,
    ),
    csv=["Engraver", "Name.engraver"],
    solr=["engraver_tesim", "engraver_sim"],
)

explicit = DluxField(
    django=ArrayField(
        TextField(),
        blank=True,
        default=list,
    ),
    csv=["Explicit"],
    solr=["explicit_tesim"],
)

extent = DluxField(
    django=ArrayField(
        TextField(),
        blank=True,
        default=list,
    ),
    csv=["Format.extent"],
    solr=["extent_tesim", "extent_sim"],
)

featured_image = DluxField(
    django=CharField(blank=True),
    csv=["Featured image"],
    solr=["featured_image_ssi"],
)

features = DluxField(
    django=ArrayField(
        TextField(),
        blank=True,
        default=list,
    ),
    csv=["Features"],
    solr=["features_tesim", "features_sim"],
)

finding_aid_url = DluxField(
    django=ArrayField(
        TextField(),
        blank=True,
        default=list,
        verbose_name="Finding aid URL",
    ),
    csv=["Finding Aid URL", "Alt ID.url"],
    solr=["finding_aid_url_ssm"],
)

foliation = DluxField(
    django=ArrayField(
        TextField(),
        blank=True,
        default=list,
    ),
    csv=["Foliation", "Foliation note"],
    solr=["foliation_tesim"],
)

folio_dimensions = DluxField(
    django=ArrayField(
        TextField(),
        blank=True,
        default=list,
    ),
    csv=["Folio dimensions", "Folio Dimensions"],
    solr=["folio_dimensions_ss"],
)

form = DluxField(
    django=ArrayField(
        TextField(),
        blank=True,
        default=list,
    ),
    csv=["Form"],
    solr=["form_tesim", "form_sim"],
)

format_book = DluxField(
    django=ArrayField(
        TextField(),
        blank=True,
        default=list,
    ),
    csv=["Format"],
    solr=["format_book_tesim"],
)

funding_note = DluxField(
    django=ArrayField(
        TextField(),
        blank=True,
        default=list,
    ),
    csv=["Description.fundingNote"],
    solr=["funding_note_tesim"],
)

genre = DluxField(
    django=ArrayField(
        TextField(),
        blank=True,
        default=list,
    ),
    csv=["Type.genre", "Genre"],
    solr=["genre_tesim", "genre_sim"],
)

hand_note = DluxField(
    django=ArrayField(
        TextField(),
        blank=True,
        default=list,
    ),
    csv=["Hand note"],
    solr=["hand_note_tesim"],
)

history = DluxField(
    django=ArrayField(
        TextField(),
        blank=True,
        default=list,
    ),
    csv=["History"],
    solr=["history_tesim"],
)

host = DluxField(
    django=ArrayField(
        TextField(),
        blank=True,
        default=list,
    ),
    csv=["Host", "Name.host"],
    solr=["host_tesim", "host_sim"],
)

identifier = DluxField(
    django=ArrayField(
        TextField(),
        blank=True,
        default=list,
    ),
    csv=["Identifier"],
    solr=["identifier_tesim"],
)

iiif_manifest_url = DluxField(
    django=CharField(blank=True, verbose_name="IIIF manifest URL"),
    csv=["IIIF Manifest URL"],
    solr=["iiif_manifest_url_ssi"],
)

iiif_range = DluxField(
    django=CharField(blank=True, verbose_name="IIIF range"),
    csv=["IIIF Range"],
    solr=["iiif_range_ssi"],
)

iiif_text_direction = DluxField(
    django=CharField(
        blank=True, choices=IIIF_TEXT_DIRECTION_CHOICES, verbose_name="IIIF text direction"
    ),
    csv=["Text direction"],
    solr=["iiif_text_direction_ssi", "human_readable_iiif_text_direction_ssi"],
)

iiif_viewing_hint = DluxField(
    django=CharField(
        blank=True,
        choices=IIIF_VIEWING_HINT_CHOICES,
        verbose_name="IIIF viewing hint",
    ),
    csv=["viewingHint"],
    solr=["human_readable_iiif_viewing_hint_ssi"],
)

illuminator = DluxField(
    django=ArrayField(
        TextField(),
        blank=True,
        default=list,
    ),
    csv=["Illuminator", "Name.illuminator"],
    solr=["illuminator_tesim", "illuminator_sim"],
)

illustrations_note = DluxField(
    django=ArrayField(
        TextField(),
        blank=True,
        default=list,
    ),
    csv=["Illustrations note", "Description.illustrations"],
    solr=["illustrations_note_tesim"],
)

illustrator = DluxField(
    django=ArrayField(
        TextField(),
        blank=True,
        default=list,
    ),
    csv=["Illustrator", "Name.illustrator"],
    solr=["illustrator_tesim", "illustrator_sim"],
)

image_count = DluxField(
    django=CharField(blank=True),
    csv=["image count"],
    solr=["image_count_ssi"],
)

incipit = DluxField(
    django=ArrayField(
        TextField(),
        blank=True,
        default=list,
    ),
    csv=["Incipit"],
    solr=["incipit_tesim"],
)

inscription = DluxField(
    django=ArrayField(
        TextField(),
        blank=True,
        default=list,
        schema=TEXTAREA_ARRAY_SCHEMA,
    ),
    csv=["Inscription"],
    solr=["inscription_tesim"],
)

interviewee = DluxField(
    django=ArrayField(
        TextField(),
        blank=True,
        default=list,
    ),
    csv=["Interviewee", "Name.interviewee"],
    solr=["interviewee_tesim", "interviewee_sim"],
)

interviewer = DluxField(
    django=ArrayField(
        TextField(),
        blank=True,
        default=list,
    ),
    csv=["Interviewer", "Name.interviewer"],
    solr=["interviewer_tesim", "interviewer_sim"],
)

language = DluxField(
    django=ArrayField(
        TextField(choices=LANGUAGE_CHOICES),
        blank=True,
        default=list,
    ),
    csv=["Language"],
    solr=[
        "language_tesim",
        "language_sim",
        "human_readable_language_tesim",  # NOTE: is filtered in `feed_ursus`
        "human_readable_language_sim",
    ],
)

latitude = DluxField(
    django=ArrayField(
        TextField(),
        blank=True,
        default=list,
    ),
    csv=["Description.latitude"],
    solr=["latitude_tesim"],
)

librettist = DluxField(
    django=ArrayField(
        TextField(),
        blank=True,
        default=list,
    ),
    csv=["Librettist"],
    solr=["librettist_tesim", "librettist_sim"],
)

license = DluxField(
    django=ArrayField(
        TextField(),
        blank=True,
        default=list,
    ),
    csv=["License"],
    solr=["license_tesim"],
)

local_identifier = DluxField(
    django=ArrayField(
        TextField(),
        blank=True,
        default=list,
    ),
    csv=[
        "Alt ID.local",
        "Alternate Identifier.local",
        "AltIdentifier.callNo",
        "AltIdentifier.local",
    ],
    solr=["local_identifier_ssim"],
)

local_rights_statement = DluxField(
    django=ArrayField(
        TextField(),
        blank=True,
        default=list,
    ),
    csv=["Rights.statementLocal"],
    solr=["local_rights_statement_ssm"],
)

location = DluxField(
    django=ArrayField(
        TextField(),
        blank=True,
        default=list,
    ),
    csv=["Coverage.geographic"],
    solr=["location_tesim", "location_sim"],
)

longitude = DluxField(
    django=ArrayField(
        TextField(),
        blank=True,
        default=list,
    ),
    csv=["Description.longitude"],
    solr=["longitude_tesim"],
)

lyricist = DluxField(
    django=ArrayField(
        TextField(),
        blank=True,
        default=list,
    ),
    csv=["Name.lyricist"],
    solr=["lyricist_tesim", "lyricist_sim"],
)

masthead_parameters = DluxField(
    django=CharField(blank=True),
    csv=["Masthead"],
    solr=["masthead_parameters_ssi"],
)

medium = DluxField(
    django=ArrayField(
        TextField(),
        blank=True,
        default=list,
    ),
    csv=["Format.medium"],
    solr=["medium_tesim", "medium_sim"],
)

musician = DluxField(
    django=ArrayField(
        TextField(),
        blank=True,
        default=list,
    ),
    csv=["Musician", "Name.musician"],
    solr=["musician_tesim", "musician_sim"],
)

named_subject = DluxField(
    django=ArrayField(
        TextField(),
        blank=True,
        default=list,
    ),
    csv=[
        "Name.subject",
        "Personal or Corporate Name.subject",
        "Subject.corporateName",
        "Subject.personalName",
    ],
    solr=["named_subject_tesim", "named_subject_sim"],
)

# TODO: This validation is currently not being used, because it is not clear how to implement it in
# a way that works with the django admin interface. It is left here for future reference.
# def longitudes_match_latitudes(longitude: list[str], latitude: list[str]) -> None:
#    """Validates that latitude and longitude pairs are properly matched."""
#    if len(latitude or []) != len(longitude or []):
#        raise ValueError(
#            "\n".join(
#                [
#                    "Mismatched lengths:",
#                    f"Latitude {latitude}",
#                    f"Longitude {longitude}",
#                ]
#            )
#        )


# TODO: Flesh out logic for validating normalized_date.
#
# For now, we are just using a RegexValidator to validate the format of `normalized_date`.
# In the future, we may need to validate that dates can actually be parsed,
# but we're deferring that, pending better understanding of variability in existing production data
# that will need to be migrated into `dlux`. (HR 8/21/26)
# def normalized_date_validator(date_str: str) -> None:
#     """Validate that the input string is a valid normalized date format.

#     This validator checks if the input string is in one of the following formats:
#     - YYYY
#     - YYYY-MM
#     - YYYY-MM-DD
#     - START_DATE/END_DATE (where both dates are in one of the above formats)

#     It also supports 3-digit years (but not fewer) and negative years, e.g., 0750 or -0750.

#     Args:
#         date_str (str): The date string to validate.

#     Raises:
#         ValidationError: If the input string is not a valid normalized date format.
#     """
#     parts = date_str.split("/")
#     if len(parts) > 2:
#         raise ValidationError(
#             "Date ranges must be in the format START_DATE/END_DATE. "
#             "They cannot have more than two parts."
#         )
#     parsed_dates: list[datetime] = []
#     for part in parts:
#         # Strip negative sign while validating year length.
#         stripped_part = part[1:] if part.startswith("-") else part
#         # Get year part if YYYY-MM or YYYY-MM-DD.
#         year_part = stripped_part.split("-")[0]
#         if not year_part.isdigit() or len(year_part) < 3:
#             raise ValidationError("Years must have a minimum of 3 digits, e.g. 750 or -1750.")

#         try:
#             parsed_date: datetime = parser.parse(part)  # type: ignore
#             parsed_dates.append(parsed_date)
#         # If either part cannot be parsed, raise ValidationError.
#         except ParserError:
#             raise ValidationError(
#                 "The provided date string(s) could not be parsed to valid dates."
#             )
#     # If there are two dates, ensure the first is not after the second,
#     # accounting for negative dates and the fact that dateutil doesn't see them as negative.
#     if len(parsed_dates) == 2:  # if it's a date range, check order
#         start_neg = parts[0].startswith("-")
#         end_neg = parts[1].startswith("-")
#         out_of_order = (
#             (not start_neg and end_neg)  # start cannot be positive if end is negative
#             or (
#                 start_neg and end_neg and parsed_dates[0] < parsed_dates[1]
#             )  # if both neg, date repr of start cannot be less than date repr of end
#             or (
#                 not start_neg and not end_neg and parsed_dates[0] > parsed_dates[1]
#             )  # if both pos, date repr of start cannot be greater than date repr of end
#         )
#         if out_of_order:
#             raise ValidationError(
#                 "In a date range, the start date must not be after the end date."
#             )


normalized_date = DluxField(
    django=ArrayField(
        TextField(
            help_text=(
                "Single date (e.g. 1980, 2020-05, 2020-05-15)or range (e.g 1980-01-04/1981-01-04). "
                "Supports 3-digit (but not fewer) and negative years (e.g. 750 or -2000)."
            ),
            validators=[
                RegexValidator(
                    regex=NORMALIZED_DATE_REGEX,
                    message=(
                        "Date must be in format YYYY, YYYY-MM, YYYY-MM-DD, or START_DATE/END_DATE. "
                        "Supports 3-digit (but not fewer) and negative years, e.g. 750 or -2000."
                    ),
                ),
                # normalized_date_validator,  # NOTE: not used currently. See TODO above.
            ],
        ),
        blank=True,
        default=list,
    ),
    csv=["Date.normalized"],
    solr=["normalized_date_tesim", "normalized_date_sim"],
)

note_admin = DluxField(
    django=ArrayField(
        TextField(),
        blank=True,
        default=list,
    ),
    csv=["AdminNote", "Description.adminnote", "Note.admin"],
    solr=["note_admin_tesim"],
)

note = DluxField(
    django=ArrayField(
        TextField(),
        blank=True,
        default=list,
    ),
    csv=["Note"],
    solr=["note_tesim"],
)

oai_set = DluxField(
    django=ArrayField(
        TextField(),
        blank=True,
        default=list,
        verbose_name="OAI set",
    ),
    csv=["oai_set"],
    solr=["oai_set_ssim"],
)

opac_url = DluxField(
    django=CharField(blank=True, verbose_name="OPAC URL"),
    csv=["Opac url", "Description.opac"],
    solr=["opac_url_ssi"],
)

other_versions = DluxField(
    django=ArrayField(
        TextField(),
        blank=True,
        default=list,
        verbose_name="Other versions",
    ),
    csv=["Other version(s)"],
    solr=["other_versions_tesim"],
)

page_layout = DluxField(
    django=ArrayField(
        TextField(),
        blank=True,
        default=list,
    ),
    csv=["Page layout"],
    solr=["page_layout_ssim"],
)

photographer = DluxField(
    django=ArrayField(
        TextField(),
        blank=True,
        default=list,
    ),
    csv=[
        "Name.photographer",
        "Personal or Corporate Name.photographer",
    ],
    solr=["photographer_tesim", "photographer_sim"],
)

place_of_origin = DluxField(
    django=ArrayField(
        TextField(),
        blank=True,
        default=list,
    ),
    csv=["Place of origin", "Publisher.placeOfOrigin"],
    solr=["place_of_origin_tesim", "place_of_origin_sim"],
)

preservation_copy = DluxField(
    django=CharField(
        blank=True,
        validators=[
            RegexValidator(
                regex=PRESERVATION_COPY_REGEX,
                message=(
                    "Preservation copy must be a path starting with 'Masters/' followed by "
                    "a subfolder and a file name, e.g. 'Masters/dlmasters/filename.tif'. "
                    "Valid subfolders are: "
                    "dlmasters, CDLI Masters, Livingstone, Maps, MEAP, or othermasters."
                ),
            )
        ],
    ),
    csv=["File Name"],
    solr=["preservation_copy_ssi"],
)

printer = DluxField(
    django=ArrayField(
        TextField(),
        blank=True,
        default=list,
    ),
    csv=["Printer", "Name.printer"],
    solr=["printer_tesim", "printer_sim"],
)

printmaker = DluxField(
    django=ArrayField(
        TextField(),
        blank=True,
        default=list,
    ),
    csv=["Printmaker", "Name.printmaker"],
    solr=["printmaker_tesim", "printmaker_sim"],
)

producer = DluxField(
    django=ArrayField(
        TextField(),
        blank=True,
        default=list,
    ),
    csv=["Producer", "Name.producer"],
    solr=["producer_tesim", "producer_sim"],
)

program = DluxField(
    django=ArrayField(
        TextField(),
        blank=True,
        default=list,
    ),
    csv=["Program"],
    solr=["program_tesim", "program_sim"],
)

provenance = DluxField(
    django=ArrayField(
        TextField(),
        blank=True,
        default=list,
        schema=TEXTAREA_ARRAY_SCHEMA,
    ),
    csv=["Provenance", "Description.history"],
    solr=["provenance_tesim"],
)

publisher = DluxField(
    django=ArrayField(
        TextField(),
        blank=True,
        default=list,
    ),
    csv=["Publisher.publisherName"],
    solr=["publisher_tesim", "publisher_sim"],
)

recipient = DluxField(
    django=ArrayField(
        TextField(),
        blank=True,
        default=list,
    ),
    csv=["Recipient", "Name.recipient"],
    solr=["recipient_tesim", "recipient_sim"],
)

# TODO: Associated this with human_readable_related_record_title_ssm
# and validate_related_record_titles()
# https://github.com/UCLALibrary/feed_ursus/blob/main/feed_ursus/ursus_solr_record.py#L1252-L1277
related_record = DluxField(
    django=ArrayField(
        TextField(),
        blank=True,
        default=list,
    ),
    csv=["Related Records"],
    solr=["related_record_ssm"],
)

related_to = DluxField(
    django=ArrayField(
        TextField(),
        blank=True,
        default=list,
    ),
    csv=["Related Items"],
    solr=["related_to_ssm"],
)

repository = DluxField(
    django=ArrayField(
        TextField(),
        blank=True,
        default=list,
    ),
    csv=[
        "repository",
        "Repository",
        "Name.repository",
        "Personal or Corporate Name.repository",
    ],
    solr=["repository_tesim", "repository_sim"],
)

representative_image = DluxField(
    django=CharField(blank=True),
    csv=["Representative image"],
    solr=["representative_image_ssi"],
)

researcher = DluxField(
    django=ArrayField(
        TextField(),
        blank=True,
        default=list,
    ),
    csv=["Researcher", "Name.researcher"],
    solr=["researcher_tesim", "researcher_sim"],
)

resource_type = DluxField(
    django=ArrayField(
        TextField(choices=RESOURCE_TYPE_CHOICES),
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

resp_statement = DluxField(
    django=ArrayField(
        TextField(),
        blank=True,
        default=list,
    ),
    csv=["Statement of Responsibility"],
    solr=["resp_statement_tesim"],
)

rights_country = DluxField(
    django=ArrayField(
        TextField(),
        blank=True,
        default=list,
    ),
    csv=["Rights.countryCreation"],
    solr=["rights_country_tesim"],
)

rights_holder = DluxField(
    django=ArrayField(
        TextField(),
        blank=True,
        default=list,
    ),
    csv=[
        "Personal or Corporate Name.copyrightHolder",
        "Rights.rightsHolderName",
    ],
    solr=["rights_holder_tesim"],
)

rights_statement = DluxField(
    django=ArrayField(
        TextField(choices=RIGHTS_STATEMENT_CHOICES),
        blank=True,
        default=list,
    ),
    csv=["Rights.copyrightStatus"],
    solr=[
        "human_readable_rights_statement_tesim",
        # TODO: has serializer in `feed_ursus`.
        # See @https://github.com/UCLALibrary/feed_ursus/blob/087cce8e3e6ef00bfdf1b84652d3883e2d43da14/feed_ursus/ursus_solr_record.py#L258
        "rights_statement_tesim",
    ],
)

rubricator = DluxField(
    django=ArrayField(
        TextField(),
        blank=True,
        default=list,
    ),
    csv=["Rubricator", "Name.rubricator"],
    solr=["rubricator_tesim", "rubricator_sim"],
)

scribe = DluxField(
    django=ArrayField(
        TextField(),
        blank=True,
        default=list,
    ),
    csv=["Scribe"],
    solr=["scribe_tesim", "scribe_sim"],
)

script = DluxField(
    django=ArrayField(
        TextField(),
        blank=True,
        default=list,
    ),
    csv=["Script"],
    solr=["script_tesim", "script_sim"],
)

script_note = DluxField(
    django=ArrayField(
        TextField(),
        blank=True,
        default=list,
        schema=TEXTAREA_ARRAY_SCHEMA,
    ),
    csv=["Script note", "Script Note"],
    solr=["script_note_tesim"],
)

series = DluxField(
    django=ArrayField(
        TextField(),
        blank=True,
        default=list,
    ),
    csv=["Series"],
    solr=["series_tesim", "series_sim"],
)

services_contact = DluxField(
    django=ArrayField(
        TextField(),
        blank=True,
        default=list,
    ),
    csv=[
        "Rights.servicesContact",
        "Rights.rightsHolderContact",
    ],
    solr=["services_contact_ssm"],
)

shelfmark = DluxField(
    django=CharField(blank=True),
    csv=["Shelfmark"],
    solr=["shelfmark_ssi"],
)

subject = DluxField(
    django=ArrayField(
        TextField(),
        blank=True,
        default=list,
    ),
    csv=["Subject"],
    solr=["subject_tesim", "subject_sim"],
)

subject_cultural_object = DluxField(
    django=ArrayField(
        TextField(),
        blank=True,
        default=list,
    ),
    csv=["Subject.culturalObject"],
    solr=["subject_cultural_object_tesim", "subject_cultural_object_sim"],
)

subject_domain_topic = DluxField(
    django=ArrayField(
        TextField(),
        blank=True,
        default=list,
    ),
    csv=["Subject.domainTopic"],
    solr=["subject_domain_topic_tesim", "subject_domain_topic_sim"],
)

subject_geographic = DluxField(
    django=ArrayField(
        TextField(),
        blank=True,
        default=list,
    ),
    csv=["Subject geographic", "Subject place"],
    solr=["subject_geographic_sim", "combined_subject_ssim"],
)

subject_temporal = DluxField(
    django=ArrayField(
        TextField(),
        blank=True,
        default=list,
    ),
    csv=["Subject temporal"],
    solr=["subject_temporal_tesim", "subject_temporal_sim"],
)

subject_topic = DluxField(
    django=ArrayField(
        TextField(),
        blank=True,
        default=list,
    ),
    csv=[
        "Subject topic",
        "Subject.conceptTopic",
        "Subject.descriptiveTopic",
    ],
    solr=["subject_topic_tesim", "subject_topic_sim"],
)

summary = DluxField(
    django=ArrayField(
        TextField(),
        blank=True,
        default=list,
        schema=TEXTAREA_ARRAY_SCHEMA,
    ),
    csv=["Summary", "Description.abstract"],
    solr=["summary_tesim"],
)

support = DluxField(
    django=ArrayField(
        TextField(),
        blank=True,
        default=list,
    ),
    csv=["Support"],
    solr=["support_tesim", "support_sim"],
)

table_of_contents = DluxField(
    django=ArrayField(
        TextField(),
        blank=True,
        default=list,
        schema=TEXTAREA_ARRAY_SCHEMA,
    ),
    csv=[
        "Table of Contents",
        "Description.tableOfContents",
    ],
    solr=["toc_tesim"],
)

tagline = DluxField(
    django=CharField(blank=True),
    csv=["Tagline"],
    solr=["tagline_ssi"],
)

thumbnail_url = DluxField(
    django=CharField(blank=True, verbose_name="Thumbnail URL"),
    csv=["Thumbnail URL", "Thumbnail"],
    solr=["thumbnail_url_ss"],
)

translator = DluxField(
    django=ArrayField(
        TextField(),
        blank=True,
        default=list,
    ),
    csv=["Translator"],
    solr=["translator_tesim", "translator_sim"],
)

uniform_title = DluxField(
    django=ArrayField(
        TextField(),
        blank=True,
        default=list,
    ),
    csv=["AltTitle.uniform"],
    solr=["uniform_title_tesim", "uniform_title_sim"],
)

# TODO: This has extensive validation logic in feed ursus for legacy CSV data, far beyond
# the official choices implemented here.  Figure out how to handle all of that.
# https://github.com/UCLALibrary/feed_ursus/blob/main/feed_ursus/ursus_solr_record.py#L266-L327
visibility = DluxField(
    django=CharField(
        blank=True,
        choices=VISIBILITY_CHOICES,
    ),
    csv=["Visibility"],
    solr=["visibility_ssi"],
)

writing_system = DluxField(
    django=ArrayField(
        TextField(),
        blank=True,
        default=list,
    ),
    csv=["Writing system"],
    solr=["writing_system_tesim", "writing_system_sim"],
)
