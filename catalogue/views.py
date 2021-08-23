from django.views import generic

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


class CartView(generic.TemplateView):
    template_name = "catalogue/modals/comparison_cart.html"

    def post(self, request, pk):
        """Add item to cart"""
        cart_content = request.session.get("cart", [])
        if pk not in cart_content and len(cart_content) <= 3:
            request.session["cart"] = cart_content + [pk]
        return self.get(request)

    def delete(self, request, pk):
        """Remove item from cart"""
        try:
            request.session["cart"].remove(pk)
        except (KeyError, ValueError):
            pass
        return self.get(request)

    def get_context_data(self, **kwargs):
        """Fetch current cart content"""
        context = super().get_context_data(**kwargs)
        context["components"] = Component.objects.filter(
            id__in=self.request.session.get("cart", [])
        )
        context["current_id"] = int(self.request.GET.get("c", -1))
        context["in_cart"] = (
            context["current_id"] in self.request.session.get("cart", [])
            or context["current_id"] == -1
        )
        return context
