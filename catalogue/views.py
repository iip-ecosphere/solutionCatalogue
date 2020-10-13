from django.http import HttpResponse
from django.shortcuts import render
from django.views import generic
from .models import Component


class IndexView(generic.ListView):
    template_name = "catalogue/index.html"
    context_object_name = "components"

    def get_queryset(self):
        return Component.objects.filter(published=True)


class DetailView(generic.DetailView):
    model = Component
    template_name = "catalogue/detail.html"

    def get_queryset(self):
        return self.model.objects.filter(published=True)
