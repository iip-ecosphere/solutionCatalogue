from django.urls import reverse
from django.views import generic

from django_filters.views import FilterView
from django.shortcuts import render

from . import COMPONENT_RELATED_FIELDS
from .forms import InquiryForm, FeedbackForm
from .filters import (
    ComponentFilter,
    ComponentFilterFrontPage,
    ComponentComparisonFilter,
)
from .models import *


class IndexView(FilterView):
    # queryset = Component.objects.filter(published=True)
    template_name = "catalogue/index.html"
    context_object_name = "components"
    filterset_class = ComponentFilterFrontPage


class SearchView(FilterView):
    template_name = "catalogue/search.html"
    context_object_name = "components"
    filterset_class = ComponentFilter

    def post(self, request, *args, **kwargs):
        view = SendFeedback.as_view()
        return view(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = FeedbackForm()
        return context


class SendFeedback(generic.edit.FormView):
    template_name = "catalogue/success_feedback.html"
    form_class = FeedbackForm

    def post(self, request, *args, **kwargs):
        self.request = request
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        feedback = form.save(commit=False)
        feedback.search_url = self.request.META["HTTP_REFERER"]
        feedback.save()
        return render(self.request, self.template_name, self.get_context_data())
    """
    def get_success_url(self):
        return reverse("catalogue:search")+'?q='+self.request.GET.get('q', '')
    """


class ComponentDetail(generic.DetailView):
    queryset = Component.objects.filter(published=True)
    template_name = "catalogue/detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = InquiryForm()
        for parent in Component.__bases__:
            context[parent.__name__.lower()+"_name"] = parent._meta.verbose_name
            context[parent.__name__.lower()
            +"_fields"] = [x.name for x in parent._meta.get_fields()]

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


class ComparisonView(FilterView):
    template_name = "catalogue/compare.html"
    context_object_name = "components"
    filterset_class = ComponentComparisonFilter
