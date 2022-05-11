from django.urls import path
from . import views

app_name = "events"

urlpatterns = [
    path("<slug:slug>", views.EventDetail.as_view(), name="event_page"),
    path("", views.EventList.as_view(), name="events"),
]