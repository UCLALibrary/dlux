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
