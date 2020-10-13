from django import template

register = template.Library()


@register.filter
def verbose_name(object):
    return object._meta.verbose_name


@register.filter
def verbose_name_plural(object):
    return object._meta.verbose_name_plural


@register.simple_tag
def get_verbose_field_name(instance, field_name):
    return instance._meta.get_field(field_name).verbose_name
