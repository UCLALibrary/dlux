"""Django models for dlux.

Our data model is defined in dlux-specific FieldGroup and DluxField objects, which should probably
be moved outside the standard django file structure. Django models are then created programmatically
from those objects.
"""

from django.db.models import (
    CASCADE,
    PROTECT,
    CharField,
    ForeignKey,
    IntegerField,
    TextField,
)

from dlux.choices import LANGUAGE_CHOICES, RESOURCE_TYPE_CHOICES
from dlux.fields import ArrayField, DluxField

TEXTAREA_ARRAY_SCHEMA = {
    "type": "list",
    "items": {
        "type": "string",
        "widget": "textarea",
    },
}

ark = DluxField(
    django=CharField(unique=True),
    csv=["Item ARK"],
    solr=["ark_ssi"],
)

collection = DluxField(
    django=ForeignKey(
        "dlux.Collection",
        on_delete=PROTECT,
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

parent = DluxField(
    django=ForeignKey(
        "dlux.Work",
        on_delete=CASCADE,
        related_name="child_works",
    ),
    csv=["Parent ARK"],
    solr=[],
)

# there's probably a library out there that we should be using
order = DluxField(
    django=IntegerField(),
    csv=[],
    solr=[],
)

title = DluxField(
    django=CharField(),
    csv=["Title"],
    solr=["title_tesim", "title_sim", "sort_title_tsort", "sort_title_ssort"],
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
