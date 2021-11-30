from django import template
from django.db.models import QuerySet

from cms.models import StaticMenuPage

register = template.Library()


@register.simple_tag
def get_top_menu_items(name: str) -> QuerySet:
    return (
        StaticMenuPage.objects.filter(menu__name=name)
        .filter(parent=None)
        .filter(published=True)
    )


@register.simple_tag
def get_child_items(parent: StaticMenuPage) -> QuerySet:
    return StaticMenuPage.objects.filter(parent=parent).filter(published=True)
