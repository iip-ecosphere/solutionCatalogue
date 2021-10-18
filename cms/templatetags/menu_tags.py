from typing import Union, List, Iterable, Tuple

from django import template
from django.db import models
from django.db.models import QuerySet
from django.db.models.fields import Field

from cms.models import StaticMenuPage

register = template.Library()


@register.simple_tag
def get_top_menu_items(name: str) -> [StaticMenuPage]:
    items = StaticMenuPage.objects.filter(menu__name=name).filter(parent=None)
    for item in items:
        yield item


@register.simple_tag
def get_child_items(parent: StaticMenuPage) -> [StaticMenuPage]:
    return StaticMenuPage.objects.filter(parent=parent)
