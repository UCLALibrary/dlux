"""Django models for dlux.

Our data model is defined in dlux-specific FieldGroup and DluxField objects, which should probably
be moved outside the standard django file structure. Django models are then created programmatically
from those objects.
"""

from django.db.models import (
    PROTECT,
    CharField,
    ForeignKey,
    IntegerField,
    TextField,
)

from dlux.choices import LANGUAGE_CHOICES, RESOURCE_TYPE_CHOICES
from dlux.fields import ArrayField, DluxField

# Used to set widget rendered in admin forms to textarea
# for longer textual fields wrapped in ArrayField
TEXTAREA_ARRAY_SCHEMA = {
    "type": "list",
    "items": {
        "type": "string",
        "widget": "textarea",
    },
}

#
#   Top fields: these will appear at the top of their respective formsets and should be defined in
#    the order we want them to appear.
#

ark = DluxField(
    django=CharField(unique=True),
    csv=["Item ARK"],
    solr=["ark_ssi"],
)

# Don't add to the model; django_polymorphic makes it automatically
# We DO need to account for it in the importer and write from the
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

title = DluxField(
    django=CharField(),
    csv=["Title"],
    solr=["title_tesim", "title_sim", "sort_title_tsort", "sort_title_ssort"],
)

#
#   Other fields: keep these alphabetized
#


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
