from django.urls import path

from . import views

app_name = "catalogue"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("component/<int:pk>/", views.DetailView.as_view(), name="detail"),
]
