from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse, reverse_lazy
from django.views import generic
from django_filters.views import FilterView

from .forms import InquiryForm
from .filters import ComponentFilter, ComponentFilterFrontPage
from .models import Component


class IndexView(FilterView):
    # queryset = Component.objects.filter(published=True)
    template_name = "catalogue/index.html"
    context_object_name = "components"
    filterset_class = ComponentFilterFrontPage


class SearchView(FilterView):
    template_name = "catalogue/search.html"
    context_object_name = "components"
    filterset_class = ComponentFilter


class ComponentDetail(generic.DetailView):
    queryset = Component.objects.filter(published=True)
    template_name = "catalogue/detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = InquiryForm()
        return context


class SendInquiry(generic.detail.SingleObjectMixin, generic.edit.FormView):
    template_name = ComponentDetail.template_name
    form_class = InquiryForm
    model = Component

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        inquiry = form.save(commit=False)
        inquiry.component = self.object
        inquiry.recipient = self.object.created_by
        inquiry.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("catalogue:detail", kwargs={"pk": self.object.pk})


class DetailView(generic.View):
    def get(self, request, *args, **kwargs):
        view = ComponentDetail.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = SendInquiry.as_view()
        return view(request, *args, **kwargs)
