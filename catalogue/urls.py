from django.urls import path
from django.views.generic import RedirectView

from . import views

app_name = "catalogue"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("search/", views.SearchView.as_view(), name="search"),
    path("component/<int:pk>/", views.DetailView.as_view(), name="detail"),
    path("compare/", views.ComparisonView.as_view(), name="compare"),
    path("admin/login/", RedirectView.as_view(url="/accounts/login/")),
    path(
        "search/feedback/", views.SearchFeedbackView.as_view(), name="search_feedback"
    ),
    path(
        "component/<int:pk>/contact", views.SendInquiry.as_view(), name="send_inquiry"
    ),
    path(
        "component/<int:pk>/report", views.ReportView.as_view(), name="report_component"
    ),
    path("cart/<int:pk>/", views.CartView.as_view(), name="edit_cart"),
    path("cart/", views.CartView.as_view(), name="get_cart"),
]
