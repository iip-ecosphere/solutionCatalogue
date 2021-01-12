from django import template

register = template.Library()


@register.filter
def verbose_name(value):
    if hasattr(value, "model"):
        value = value.model
    return value._meta.verbose_name


@register.filter
def verbose_name_plural(value):
    if hasattr(value, "model"):
        value = value.model
    return value._meta.verbose_name_plural


@register.simple_tag
def get_verbose_field_name(instance, field_name):
    if hasattr(instance, "model"):
        instance = instance.model
    return instance._meta.get_field(field_name).verbose_name
