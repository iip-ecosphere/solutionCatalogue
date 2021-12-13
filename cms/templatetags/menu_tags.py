from typing import Iterable

from django import template
from django.db.models import QuerySet

from cms.models import StaticMenuPage

register = template.Library()


@register.simple_tag
def get_top_menu_items(name: str) -> Iterable[StaticMenuPage]:
    qs = (
        StaticMenuPage.objects.filter(menu__name=name)
        .filter(parent=None)
        .filter(published=True)
    )
    # remove sites that are root points but have no children sites
    for item in qs:
        if not item.root or len(get_child_items(item)) > 0:
            yield item


@register.simple_tag
def get_child_items(parent: StaticMenuPage) -> QuerySet:
    return StaticMenuPage.objects.filter(parent=parent).filter(published=True)
