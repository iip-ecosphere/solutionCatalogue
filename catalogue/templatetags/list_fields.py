from django import template

register = template.Library()


@register.simple_tag
def list_fields(object):
    for field in object._meta.get_fields():
        if field.auto_created or field.is_relation:
            continue
        if field.choices:
            choice = [
                c for i, c in field.choices if i == field.value_from_object(object)
            ][0]
            yield field.verbose_name, choice
        else:
            yield field.verbose_name, field.value_to_string(object)
