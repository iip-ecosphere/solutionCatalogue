from typing import Union, List, Iterable, Tuple

from django import template
from django.db import models
from django.db.models import QuerySet
from django.db.models.fields import Field

from cms.models import StaticMenuPage

register = template.Library()


@register.simple_tag
def get_top_menu_items(name: str) -> List[StaticMenuPage]:
    return StaticMenuPage.objects.filter(menu__name=name).filter(parent=None)


@register.simple_tag
def get_child_items(parent: StaticMenuPage) -> List[StaticMenuPage]:
    return StaticMenuPage.objects.filter(parent=parent)
