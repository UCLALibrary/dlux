"""Type stub for django_jsonform ArrayField.

Pieced together from:
https://github.com/typeddjango/django-stubs/blob/6.0.7/django-stubs/contrib/postgres/fields/array.pyi
from https://github.com/H4rryK4ne/django-jsonform-stubs/blob/459762a/django_jsonform-stubs/utils.pyi
https://github.com/bhch/django-jsonform/blob/e485ef149902962a5b9ec83bcb1150ffbee64ef6/django_jsonform/models/fields.py#L53-L68
"""

# pyright: reportPrivateUsage=false

from collections.abc import Iterable, Sequence
from typing import Any, ClassVar, Literal, Required, TypedDict, Union

from django.contrib.postgres.utils import CheckPostgresInstalledMixin
from django.core.validators import _ValidatorCallable
from django.db.models import Field
from django.db.models.expressions import Combinable, Expression
from django.db.models.fields import _ErrorMessagesDict, _ErrorMessagesMapping
from django.db.models.fields.mixins import CheckFieldDefaultMixin
from django.utils.choices import _Choices
from django.utils.functional import _StrOrPromise
from typing_extensions import TypeVar

#

class TitledStringChoice(TypedDict):
    title: _StrOrPromise
    value: str

class TitledNumberChoice(TypedDict):
    title: _StrOrPromise
    value: float

class TitledIntegerChoice(TypedDict):
    title: _StrOrPromise
    value: int

class TitledBooleanChoice(TypedDict):
    title: _StrOrPromise
    value: bool

class LabeledStringChoice(TypedDict):
    label: _StrOrPromise
    value: str

class LabeledNumberChoice(TypedDict):
    label: _StrOrPromise
    value: float

class LabeledIntegerChoice(TypedDict):
    label: _StrOrPromise
    value: int

class LabeledBooleanChoice(TypedDict):
    label: _StrOrPromise
    value: bool

BooleanChoices = Sequence[Union[bool, TitledBooleanChoice, LabeledBooleanChoice]]
NumberChoices = Sequence[Union[float, TitledNumberChoice, LabeledNumberChoice]]
IntegerChoices = Sequence[Union[int, TitledIntegerChoice, LabeledIntegerChoice]]
StringChoices = Sequence[Union[str, TitledStringChoice, LabeledStringChoice]]
AnyChoices = Union[BooleanChoices, NumberChoices, IntegerChoices, StringChoices]

class BaseFieldSchema(TypedDict, total=False):
    title: _StrOrPromise

class ArraySchema(BaseFieldSchema, total=False):
    type: Required[Literal["array", "list"]]
    items: Required[InputFieldSchema]
    default: Any
    minItems: int
    min_items: int
    maxItems: int
    max_items: int
    uniqueItems: bool

class ObjectSchema(BaseFieldSchema, total=False):
    type: Required[Literal["object", "dict"]]
    properties: dict[str, AnySchema]
    keys: dict[str, AnySchema]
    required: Sequence[str]
    additionalProperties: Union[bool, AnySchema]
    oneOf: list[Any]  # TODO
    anyOf: list[Any]  # TODO
    allOf: list[Any]  # TODO

class BaseInputFieldSchema(BaseFieldSchema, total=False):
    help_text: _StrOrPromise
    helpText: _StrOrPromise  # alias for help_text
    required: bool

class StringSchema(BaseInputFieldSchema, total=False):
    type: Required[Literal["string"]]
    format: Literal[
        "color",
        "date",
        "date-time",
        "datetime",  # alias date-time
        "email",
        "password",
        "time",
        "data-url",
        "file-url",
        "uri",
        "uri-reference",
    ]
    enum: StringChoices
    choices: StringChoices  # alias for enum
    widget: Literal[
        "textarea",
        "radio",
        "autocomplete",
        "multiselect",  # only valid, if hold in an array
        "multiselect-autocomplete",
        "fileinput",
        "hidden",
    ]
    default: str
    readonly: bool
    readOnly: bool  # alias for readonly
    placeholder: str
    minLength: int
    maxLength: int
    handler: str

class NumberSchema(BaseInputFieldSchema, total=False):
    type: Required[Literal["number"]]
    choices: NumberChoices
    enum: NumberChoices  # alias for choices
    widget: Literal["range"]
    default: float
    readonly: bool
    readOnly: bool  # alias for readonly
    placeholder: float
    minimum: float
    maximum: float
    exclusiveMinimum: float
    exclusiveMaximum: float

class IntegerSchema(BaseInputFieldSchema, total=False):
    type: Required[Literal["integer"]]
    choices: IntegerChoices
    enum: IntegerChoices  # alias for choices
    widget: Literal["range"]
    default: int
    readonly: bool
    readOnly: bool  # alias for readonly
    placeholder: int
    minimum: int
    maximum: int
    exclusiveMinimum: int
    exclusiveMaximum: int

class BooleanSchema(BaseInputFieldSchema, total=False):
    type: Required[Literal["boolean"]]
    choices: BooleanChoices
    enum: BooleanChoices  # alias for choices
    widget: Literal["radio", "select"]
    default: bool
    readonly: bool
    readOnly: bool  # alias for readonly

class ConstSchema(BaseFieldSchema, total=False):
    const: Required[_StrOrPromise]

InputFieldSchema = Union[
    StringSchema,
    NumberSchema,
    IntegerSchema,
    BooleanSchema,
    ConstSchema,
]
Reference = TypedDict("Reference", {"$ref": str})

class OneOfSchema(TypedDict):
    # TODO:
    pass

class AnyOfSchema(TypedDict):
    # TODO:
    pass

class AllOfSchema(TypedDict):
    # TODO:
    pass

AnySchema = Union[InputFieldSchema, ArraySchema, ObjectSchema, Reference]
RootSchema = Union[ArraySchema, ObjectSchema]

# from django-stubs

class NOT_PROVIDED: ...

# __set__ value type
_ST = TypeVar("_ST")
# __get__ return type
_GT = TypeVar("_GT")

class ArrayField(CheckPostgresInstalledMixin, CheckFieldDefaultMixin, Field[_ST, _GT]):
    _pyi_private_set_type: Sequence[Any] | Combinable
    _pyi_private_get_type: list[Any]

    empty_strings_allowed: bool
    default_error_messages: ClassVar[_ErrorMessagesDict]
    base_field: Field[Any, Any]
    name: str
    size: int | None
    default_validators: list[_ValidatorCallable]
    from_db_value: Any
    def __init__(  # pyright: ignore[reportArgumentType]
        self,
        base_field: Field,  # pyright: ignore[reportMissingTypeArgument, reportUnknownParameterType]
        size: int | None = None,
        *,
        nested: bool = ...,
        schema: ArraySchema = ...,
        verbose_name: _StrOrPromise | None = ...,
        name: str | None = ...,
        primary_key: bool = ...,
        max_length: int | None = ...,
        unique: bool = ...,
        blank: bool = ...,
        null: bool = ...,
        db_index: bool = ...,
        default: Any = ...,
        db_default: type[NOT_PROVIDED] | Expression | _ST = ...,  # pyright: ignore[reportInvalidTypeVarUse]
        editable: bool = ...,
        auto_created: bool = ...,
        serialize: bool = ...,
        unique_for_date: str | None = ...,
        unique_for_month: str | None = ...,
        unique_for_year: str | None = ...,
        choices: _Choices | None = ...,
        help_text: _StrOrPromise = ...,
        db_column: str | None = ...,
        db_comment: str | None = ...,
        db_tablespace: str | None = ...,
        validators: Iterable[_ValidatorCallable] = ...,
        error_messages: _ErrorMessagesMapping | None = ...,
    ) -> None: ...
    # @override
    # def check(self, **kwargs: Any) -> list[CheckMessage]: ...
    # @property
    # @override
    # def description(self) -> str: ...  # type: ignore[override]
    # @override
    # def cast_db_type(self, connection: BaseDatabaseWrapper) -> str: ...
    # def get_placeholder(
    #     self, value: Unused, compiler: Unused, connection: BaseDatabaseWrapper
    # ) -> str: ...
    # @override
    # # def get_transform(self, name: str) -> type[Transform] | None: ...
    # def formfield(
    #     self,
    #     *,
    #     nested: bool = ...,
    #     schema: ArraySchema = ...,
    #     form_class: type[forms.Field] | None = ...,
    #     choices_form_class: type[forms.ChoiceField] | None = ...,
    #     required: bool = ...,
    #     widget: Widget | type[Widget] | None = ...,
    #     label: _StrOrPromise | None = ...,
    #     initial: Any | None = ...,
    #     help_text: _StrOrPromise = ...,
    #     error_messages: _ErrorMessagesMapping | None = ...,
    #     show_hidden_initial: bool = ...,
    #     validators: Iterable[_ValidatorCallable] = ...,
    #     localize: bool = ...,
    #     disabled: bool = ...,
    #     label_suffix: str | None = ...,
    #     **kwargs: Any,
    #     # Subclasses are allowed to return None
    # ) -> forms.Field | None: ...
