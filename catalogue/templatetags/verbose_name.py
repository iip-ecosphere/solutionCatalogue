from django import template
from django.db import models

register = template.Library()


@register.simple_tag
@register.filter
def verbose_name(m: models.Model) -> str:
    """Return verbose name of a model or relation"""
    if hasattr(m, "model"):
        m = m.model
    return m._meta.verbose_name


@register.filter
def verbose_name_plural(m: models.Model) -> str:
    """Return plural verbose name of a model or relation"""
    if hasattr(m, "model"):
        m = m.model
    return m._meta.verbose_name_plural
