from django import template
from django.db import models

register = template.Library()


@register.filter
def verbose_name(m) -> str:
    """Return verbose name of a model or relation"""
    if hasattr(m, "model"):
        m = m.model
    return m._meta.verbose_name


@register.filter
def verbose_name_plural(m) -> str:
    """Return plural verbose name of a model or relation"""
    if hasattr(m, "model"):
        m = m.model
    return m._meta.verbose_name_plural


@register.simple_tag
def get_verbose_field_name(model: models.Model, field_name: str) -> str:
    """Return verbose name of a model field"""
    if hasattr(model, "model"):
        model = model.model
    return model._meta.get_field(field_name).verbose_name
