from typing import Union, List

from django import template
from django.db import models
from django.db.models import QuerySet

register = template.Library()


@register.simple_tag
def field_value(m: models.Model, field_name: str) -> Union[str, List[str], QuerySet]:
    """Return value of a model field"""
    field = m._meta.get_field(field_name)
    if hasattr(m, f"{field_name}_set"):
        # related field
        return getattr(m, f"{field_name}_set").all()
    elif field.choices:
        # choices field
        return [c for i, c in field.choices if i == field.value_from_object(m)][0]
    else:
        return field.value_to_string(m)


@register.simple_tag
def field_verbose_name(m: models.Model, field_name: str) -> str:
    """Return verbose name of a model field"""
    related_field = [
        f
        for f in m._meta.get_fields()
        if f.name == field_name and isinstance(f, models.ForeignObjectRel)
    ]
    if related_field:
        # get name of related model for related fields
        return related_field[0].related_model._meta.verbose_name

    if hasattr(m, "model"):
        m = m.model
    return m._meta.get_field(field_name).verbose_name
