from django.urls import path
from . import views

app_name = "cms"

urlpatterns = [
    path("<str:page_url>", views.PageView.as_view(), name="page"),
]
