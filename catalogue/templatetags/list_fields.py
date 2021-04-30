from django import template
from django.db import models

register = template.Library()


@register.simple_tag
def list_fields(object):
    """Extract all field names and values for an object."""
    for field in object._meta.get_fields():
        if field.auto_created or field.is_relation:
            continue
        elif field.choices:
            choice = [
                c for i, c in field.choices if i == field.value_from_object(object)
            ][0]
            yield field.verbose_name, choice
        else:
            yield field.verbose_name, field.value_to_string(object)
    # display multi-value after single
    for field in object._meta.get_fields():
        if isinstance(field, models.ForeignObjectRel):
            yield field.related_model._meta.verbose_name, getattr(object, field.name + "_set").all()
