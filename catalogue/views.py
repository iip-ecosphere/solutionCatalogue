from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django_filters.views import FilterView

from .models import Component
from .filters import ComponentFilter


class IndexView(generic.ListView):
    queryset = Component.objects.filter(published=True)
    template_name = "catalogue/index.html"
    context_object_name = "components"


class SearchView(FilterView):
    template_name = "catalogue/search.html"
    context_object_name = "components"
    filterset_class = ComponentFilter


class DetailView(generic.DetailView):
    queryset = Component.objects.filter(published=True)
    template_name = "catalogue/detail.html"


class RegisterView(generic.CreateView):
    template_name = "catalogue/registration/register.html"
    form_class = UserCreationForm
    success_url = reverse_lazy("catalogue:login")
