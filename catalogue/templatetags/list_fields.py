from typing import Union, List, Iterable, Tuple

from django import template
from django.db import models
from django.db.models import QuerySet
from django.db.models.fields import Field

register = template.Library()


def get_fields(m: models.Model) -> List[Field]:
    """Return direct fields of a model"""
    return [f for f in m._meta.get_fields() if not (f.auto_created or f.is_relation)]


def get_related_fields(m: models.Model) -> List[models.ForeignObjectRel]:
    """Return related fields of a model"""
    return [f for f in m._meta.get_fields() if isinstance(f, models.ForeignObjectRel)]


@register.simple_tag
def list_fields(
    m: models.Model, field_filter: List[str]
) -> Iterable[Union[str, List[str], QuerySet]]:
    """Extract model field names and values for the given field list."""
    for field in [f for f in get_fields(m) if f.name in field_filter]:
        if field.choices:
            choice = [c for i, c in field.choices if i == field.value_from_object(m)][0]
            yield field.verbose_name, choice
        else:
            yield field.verbose_name, field.value_to_string(m)
    # display multi-value after single
    for field in [f for f in get_related_fields(m) if f.name in field_filter]:
        yield field.related_model._meta.verbose_name, getattr(
            m, field.name + "_set"
        ).all()


@register.simple_tag
def list_field_names(m: models.Model) -> Iterable[Tuple[str, str]]:
    """Return field names of a model"""
    for field in get_fields(m):
        yield field.verbose_name, field.name
    # display multi-value after single
    for field in get_related_fields(m):
        yield field.related_model._meta.verbose_name, field.name


@register.simple_tag
def get_field(m: models.Model, field_name: str) -> str:
    """Return value of a field in a model"""
    field = m._meta.get_field(field_name)
    if field.choices:
        choice = [c for i, c in field.choices if i == field.value_from_object(m)][0]
        return choice
    else:
        return field.value_to_string(m)


@register.simple_tag
def get_related_field(m: models.Model, field: str) -> QuerySet:
    """Return related objects for a field in a model"""
    return getattr(m, field + "_set").all()


@register.simple_tag
def check_category_empty(m: models.Model, field_names: List[str]) -> bool:
    """Check if all given fields are empty"""
    return not any(m._meta.get_field(name) for name in field_names)
