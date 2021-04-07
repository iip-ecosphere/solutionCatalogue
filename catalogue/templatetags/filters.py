from django import template
from django.db.models import QuerySet

register = template.Library()


@register.filter
def is_list(val):
    return isinstance(val, list) or isinstance(val, QuerySet)
