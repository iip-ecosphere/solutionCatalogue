from django.urls import reverse
from django.views import generic, View

from django_filters.views import FilterView
from django.shortcuts import render
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.auth import get_user_model
from django.conf import settings
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = FeedbackForm()
        return context


class SearchFeedbackView(generic.edit.FormView):
    template_name = "catalogue/modals/search-feedback/form.html"
    success_template = "catalogue/modals/search-feedback/success.html"
    form_class = FeedbackForm

    def post(self, request, *args, **kwargs):
        self.request = request
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        feedback = form.save(commit=False)
        feedback.search_url = self.request.META["HTTP_REFERER"]
        feedback.save()
        self.send_mail_feedback(feedback)
        return render(self.request, self.success_template, self.get_context_data())

    def send_mail_feedback(self, form):
        User = get_user_model()
        admin_emails = User.objects.filter(is_superuser=True).values_list(
            "email", flat=True
        )

        context = {
            "name": form.name,
            "message": form.message,
            "email": form.mail,
            "sentiment": form.sentiment,
        }
        content = render_to_string("catalogue/emails/email_feedback.txt", context)
        send_mail(
            subject="IIP Ecosphere Lösungskatalog: Feedback",
            message=content,
            from_email=settings.SENDER_EMAIL_FEEDBACK,
            recipient_list=admin_emails,
        )


class DetailView(generic.DetailView):
    queryset = Component.objects.filter(published=True)
    template_name = "catalogue/detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = InquiryForm()
        return context


class SendInquiry(generic.detail.SingleObjectMixin, generic.edit.FormView):
    http_method_names = ["post"]
    template_name = "catalogue/modals/contact/success.html"
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
        self.send_mail_customer(inquiry, self.object)
        return render(self.request, self.template_name)

    def send_mail_customer(self, form, obj):
        context = {
            "name": form.name,
            "message": form.message,
            "email": form.mail,
            "comp": obj,
        }
        content = render_to_string("catalogue/emails/email_message.txt", context)
        send_mail(
            subject="IIP Ecosphere Lösungskatalog: Anfrage",
            message=content,
            from_email=settings.SENDER_EMAIL_MESSAGE,
            recipient_list=[obj.created_by.email],
        )


class ComparisonView(FilterView):
    template_name = "catalogue/compare.html"
    context_object_name = "components"
    filterset_class = ComponentComparisonFilter

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for parent in Component.__bases__:
            context[parent.__name__.lower() + "_fields"] = [
                x.name for x in parent._meta.get_fields()
            ]

        return context


class CartView(View):
    def post(self, request, pk):
        if pk not in request.session["cart"] and len(request.session["cart"]) <= 3:
            request.session["cart"].append(pk)
        return self.get(request)

    def delete(self, request, pk):
        print(int(request.GET.get("c", -1)))
        request.session["cart"].remove(pk)
        return self.get(request)

    def get(self, request):
        if "cart" not in request.session:
            request.session["cart"] = []
        c_pk = int(request.GET.get("c", -1))  # current component
        in_cart = c_pk in request.session["cart"] or c_pk == -1
        components = Component.objects.filter(id__in=request.session["cart"])
        return render(
            request,
            "catalogue/modals/compare/compare_button.html",
            {"components": components, "c_pk": c_pk, "in_cart": in_cart},
        )
