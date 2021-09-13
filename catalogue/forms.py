from django.forms import ModelForm, Textarea
from .models.messages import Inquiry, Feedback, Report


class InquiryForm(ModelForm):
    class Meta:
        model = Inquiry
        widgets = {
            "message": Textarea(attrs={"rows": 4, "cols": 15}),
        }
        fields = ("name", "mail", "message")


class FeedbackForm(ModelForm):
    class Meta:
        model = Feedback
        widgets = {
            "message": Textarea(attrs={"rows": 4, "cols": 15}),
        }
        fields = ("name", "mail", "sentiment", "message")


class ReportForm(ModelForm):
    class Meta:
        model = Report
        widgets = {
            "message": Textarea(attrs={"rows": 4, "cols": 15}),
        }
        fields = ("name", "mail", "message")
