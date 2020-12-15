from django.forms import ModelForm
from .models.messages import Inquiry


class InquiryForm(ModelForm):
    class Meta:
        model = Inquiry
        exclude = ["created", "recipient", "component"]
