from django.forms import ModelForm, Textarea
from .models.messages import Inquiry, Feedback


class InquiryForm(ModelForm):
    class Meta:
        model = Inquiry
        widgets = {
            "message": Textarea(attrs={"rows": 4, "cols": 15}),
        }
        exclude = ["created", "recipient", "component"]


class FeedbackForm(ModelForm):
    class Meta:
        model = Feedback
        widgets = {
            "message": Textarea(attrs={"rows": 4, "cols": 15}),
        }
        exclude = ["created", "recipient", "search_url"]
