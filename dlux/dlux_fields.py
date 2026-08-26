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
    URLField,
)

from dlux.choices import IIIF_VIEWING_HINT_CHOICES, LANGUAGE_CHOICES, RESOURCE_TYPE_CHOICES
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
# Matches path-like strings with particular folder structure.
PRESERVATION_COPY_REGEX = r"^Masters/(dlmasters|CDLIMasters|Livingstone|Maps|MEAP|othermasters)/.*"


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
    django=URLField(blank=True, null=True),
    csv=[
        "access_copy",
        "IIIF Access URL",
    ],
    solr=["access_copy_ssi"],
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

genre = DluxField(
    django=ArrayField(
        TextField(),
        blank=True,
        default=list,
    ),
    csv=["Type.genre", "Genre"],
    solr=["genre_tesim", "genre_sim"],
)

iiif_manifest_url = DluxField(
    django=CharField(blank=True, null=True),
    csv=["IIIF Manifest URL"],
    solr=["iiif_manifest_url_ssi"],
)

iiif_viewing_hint = DluxField(
    django=CharField(blank=True, null=True, choices=IIIF_VIEWING_HINT_CHOICES),
    csv=["viewingHint"],
    solr=["human_readable_iiif_viewing_hint_ssi"],
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

preservation_copy = DluxField(
    django=CharField(
        blank=True,
        null=True,
        validators=[
            RegexValidator(
                regex=PRESERVATION_COPY_REGEX,
                message=(
                    "Preservation copy must be a path starting with 'Masters/' "
                    "followed by one of the following subfolders: "
                    "dlmasters, CDLI Masters, Livingstone, Maps, MEAP, or othermasters."
                ),
            )
        ],
    ),
    csv=["File Name"],
    solr=["preservation_copy_ssi"],
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

subject = DluxField(
    django=ArrayField(
        TextField(),
        blank=True,
        default=list,
    ),
    csv=["Subject"],
    solr=["subject_tesim", "subject_sim"],
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

thumbnail_url = DluxField(
    django=CharField(blank=True, null=True),
    csv=["Thumbnail URL", "Thumbnail"],
    solr=["thumbnail_url_ss"],
)
