from django.views import generic
from django.shortcuts import render
from django.conf import settings
from django.shortcuts import get_object_or_404
from .models import StaticMenuPage
import pathlib


class PageView(generic.DetailView):
    model = StaticMenuPage
    context_object_name = "page"

    def get_template_names(self):
        return [pathlib.Path(__file__).parent / "templates" / self.object.template]
