import os
from django.conf import settings
from django.contrib.sites.models import Site
from django.core.mail import send_mail
from django.http.response import FileResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.views import generic
from django_filters.views import FilterView
from django.http import HttpResponse, Http404

from .filters import (
    ComponentFilter,
    ComponentFilterBase,
    ComponentComparisonFilter,
)
from .forms import InquiryForm, FeedbackForm, ReportForm
from .models import Component, ComponentFile
from .models.logging import SearchLog, ComponentLog
from .models.messages import Inquiry, Feedback, Report
from .utils import is_admin_or_mod, get_admin_emails, get_mod_emails


class IndexView(FilterView):
    template_name = "catalogue/index.html"
    context_object_name = "components"
    queryset = Component.public_objects.filter(frontpage=True)
    filterset_class = ComponentFilterBase


class SearchView(FilterView):
    template_name = "catalogue/search.html"
    context_object_name = "components"
    queryset = Component.public_objects.all()
    filterset_class = ComponentFilter

    def get(self, request, *args, **kwargs):
        # check if user has session and save query
        if not request.session or not request.session.session_key:
            request.session.save()
        log = SearchLog.objects.create(
            query=request.get_full_path(),
            identifier=request.session.session_key,
            query_result_count=self.queryset.count(),
        )
        # Save SearchLog in session for component relation
        request.session["current_query"] = log.id
        return super().get(request, *args, **kwargs)

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

    def send_mail_feedback(self, feedback: Feedback):
        content = render_to_string(
            "catalogue/emails/email_feedback.txt",
            {
                "feedback": feedback,
            },
            request=self.request,
        )
        send_mail(
            subject=f"{Site.objects.get_current().name}: Feedback",
            message=content,
            from_email=settings.SENDER_EMAIL_FEEDBACK,
            recipient_list=get_admin_emails(),
        )


class DetailView(generic.DetailView):
    template_name = "catalogue/detail.html"
    model = Component

    def get(self, request, *args, **kwargs):
        ret = super().get(request, *args, **kwargs)
        if "current_query" in request.session:
            # log user access on component after search
            ComponentLog(
                query=SearchLog.objects.get(pk=request.session["current_query"]),
                component=self.object,
            ).save()
        return ret

    def get_queryset(self):
        qs = super().get_queryset()
        comp = qs.get(id=self.kwargs.get(self.pk_url_kwarg))
        if self.request.GET.get("preview", None) and (
            comp.created_by == self.request.user or is_admin_or_mod(self.request)
        ):
            # allow preview of components for owners or mods
            return qs

        return Component.public_objects.all()

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
        inquiry.save()
        self.send_mail_customer(inquiry)
        return render(self.request, self.template_name)

    def send_mail_customer(self, inquiry: Inquiry):
        content = render_to_string(
            "catalogue/emails/email_message.txt",
            {
                "inquiry": inquiry,
            },
            request=self.request,
        )
        send_mail(
            subject=f"{Site.objects.get_current().name}: Anfrage",
            message=content,
            from_email=settings.SENDER_EMAIL_MESSAGE,
            recipient_list=[inquiry.component.contact_email],
        )


class ComparisonView(FilterView):
    template_name = "catalogue/compare.html"
    context_object_name = "components"
    queryset = Component.public_objects.all()
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


class ReportView(generic.detail.SingleObjectMixin, generic.edit.FormView):
    template_name = "catalogue/modals/report/form.html"
    success_template = "catalogue/modals/report/success.html"
    form_class = ReportForm
    model = Component

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        report = form.save(commit=False)
        report.component = self.object
        report.save()
        self.send_mail_report(report)
        return render(self.request, self.success_template, self.get_context_data())

    def send_mail_report(self, report: Report):
        content = render_to_string(
            "catalogue/emails/email_report.txt",
            {
                "report": report,
            },
            request=self.request,
        )
        send_mail(
            subject=f"{Site.objects.get_current().name}: Report",
            message=content,
            from_email=settings.SENDER_EMAIL_FEEDBACK,
            recipient_list=get_mod_emails(),
        )


def downloadMedia(request, id):
    path = ComponentFile.objects.get(id=id).file.path
    if os.path.exists(path):
        response = FileResponse(open(path, "rb"), as_attachment=True)
        return response
    raise Http404("Datei nicht gefunden")
