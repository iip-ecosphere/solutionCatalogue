from typing import Any

from django import template
from django.db.models import QuerySet

register = template.Library()


@register.filter
def is_list(val: Any) -> bool:
    """Check if something is a list"""
    return isinstance(val, list) or isinstance(val, QuerySet)
