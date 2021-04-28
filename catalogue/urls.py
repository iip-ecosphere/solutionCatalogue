from django.urls import path, include
from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView

from . import views

app_name = "catalogue"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("search/", views.SearchView.as_view(), name="search"),
    path("component/<int:pk>/", views.DetailView.as_view(), name="detail"),
    path("admin/login/", RedirectView.as_view(url="/accounts/login/")),
]
