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
    m: models.Model,
) -> Iterable[Union[str, List[str], QuerySet]]:
    """Extract all field names and values for a model."""
    for field in get_fields(m):
        if field.choices:
            choice = [c for i, c in field.choices if i ==
                      field.value_from_object(m)][0]
            yield field.verbose_name, choice
        else:
            yield field.verbose_name, field.value_to_string(m)
    # display multi-value after single
    for field in get_related_fields(m):
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
def get_field(m: models.Model, field: str) -> str:
    """Return value of a field in a model"""
    related_fields = set(f.name for f in get_related_fields(m))
    if field in related_fields:
        return ", ".join(str(x) for x in getattr(m, field + "_set").all())
    elif field := m._meta.get_field(field):
        if field.choices:
            choice = [c for i, c in field.choices if i ==
                      field.value_from_object(m)][0]
            return choice
        else:
            return field.value_to_string(m)


@register.simple_tag
def get_related_field_value(m: models.Model, field: str):
    return getattr(m, field + "_set").all()


@register.simple_tag
def check_category_empty(m: models, field_names: List) -> bool:
    for name in field_names:
        field = m._meta.get_field(name)
        if field is not None:
            return False
    return True
