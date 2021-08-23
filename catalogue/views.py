from django.views import generic

from django_filters.views import FilterView
from django.shortcuts import render
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.auth import get_user_model
from django.conf import settings

from . import COMPONENT_RELATED_FIELDS
from .forms import InquiryForm, FeedbackForm, ReportForm
from .filters import (
    ComponentFilter,
    ComponentFilterFrontPage,
    ComponentComparisonFilter,
)
from .models import *
from .models.messages import Inquiry, Feedback


class IndexView(FilterView):
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

    def form_valid(self, form: FeedbackForm):
        feedback = form.save(commit=False)
        feedback.search_url = self.request.META["HTTP_REFERER"]
        feedback.save()
        self.send_mail_feedback(feedback)
        return render(self.request, self.success_template, self.get_context_data())

<<<<<<< HEAD
    def send_mail_feedback(self, form):
        User = get_user_model()
        admin_emails = User.objects.filter(is_superuser=True).values_list(
            "email", flat=True
        )

=======
    def send_mail_feedback(self, feedback: Feedback):
>>>>>>> upstream/main
        context = {
            "name": feedback.name,
            "message": feedback.message,
            "email": feedback.mail,
            "sentiment": feedback.sentiment,
        }
        content = render_to_string("catalogue/emails/email_feedback.txt", context)
        admin_emails = (
            get_user_model()
            .objects.filter(is_superuser=True)
            .values_list("email", flat=True)
        )
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

    def form_valid(self, form: InquiryForm):
        inquiry = form.save(commit=False)
        inquiry.component = self.get_object()
        inquiry.recipient = inquiry.component.created_by
        inquiry.save()
        self.send_mail_customer(inquiry)
        return render(self.request, self.template_name)

    def send_mail_customer(self, inquiry: Inquiry):
        context = {
            "name": inquiry.name,
            "message": inquiry.message,
            "email": inquiry.mail,
            "comp": inquiry.component,
        }
        content = render_to_string("catalogue/emails/email_message.txt", context)
        send_mail(
            subject="IIP Ecosphere Lösungskatalog: Anfrage",
            message=content,
            from_email=settings.SENDER_EMAIL_MESSAGE,
            recipient_list=[inquiry.recipient.email],
        )


class ComparisonView(FilterView):
    template_name = "catalogue/compare.html"
    context_object_name = "components"
    filterset_class = ComponentComparisonFilter

<<<<<<< HEAD

class ReportView(generic.detail.SingleObjectMixin, generic.edit.FormView):
    template_name = "catalogue/modals/report/form.html"
    success_template = "catalogue/modals/report/success.html"
    form_class = ReportForm
    model = Component

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.request = request
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        report = form.save(commit=False)
        report.component = self.object
        report.save()
        self.send_mail_report(report)
        return render(self.request, self.success_template, self.get_context_data())

    def send_mail_report(self, form):
        User = get_user_model()
        admin_emails = User.objects.filter(is_superuser=True).values_list(
            "email", flat=True
        )

        context = {
            "name": form.name,
            "message": form.message,
            "email": form.mail,
            "component": form.component,
        }
        content = render_to_string("catalogue/emails/email_report.txt", context)
        send_mail(
            subject="IIP Ecosphere Lösungskatalog: Report",
            message=content,
            from_email=settings.SENDER_EMAIL_FEEDBACK,
            recipient_list=admin_emails,
        )
=======
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for parent in Component.__bases__:
            context[parent.__name__.lower() + "_fields"] = [
                x.name for x in parent._meta.get_fields()
            ]

        return context


class CartView(generic.TemplateView):
    template_name = "catalogue/modals/comparison_cart.html"

    def post(self, request, pk: int):
        """Add item to cart"""
        cart_content = request.session.get("cart", [])
        if pk not in cart_content and len(cart_content) <= 3:
            request.session["cart"] = cart_content + [pk]
        return self.get(request)

    def delete(self, request, pk: int):
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
>>>>>>> upstream/main
