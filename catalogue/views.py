from django.views import generic
from .models import Component
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy


class IndexView(generic.ListView):
    queryset = Component.objects.filter(published=True)
    template_name = "catalogue/index.html"
    context_object_name = "components"


class DetailView(generic.DetailView):
    queryset = Component.objects.filter(published=True)
    template_name = "catalogue/detail.html"


class RegisterView(generic.CreateView):
    template_name = "catalogue/registration/register.html"
    form_class = UserCreationForm
    success_url = reverse_lazy("catalogue:login")
