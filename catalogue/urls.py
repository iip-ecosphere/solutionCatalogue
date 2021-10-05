from django.urls import path
from django.views.generic import RedirectView

from . import views

app_name = "catalogue"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("admin/login/", RedirectView.as_view(url="/accounts/login/")),
    path("search", views.SearchView.as_view(), name="search"),
    path("search/feedback", views.SearchFeedbackView.as_view(), name="search_feedback"),
    path("solution/<int:pk>", views.DetailView.as_view(), name="detail"),
    path("solution/<int:pk>/contact", views.SendInquiry.as_view(), name="send_inquiry"),
    path(
        "solution/<int:pk>/report", views.ReportView.as_view(), name="report_component"
    ),
    path("compare", views.ComparisonView.as_view(), name="compare"),
    path("cart/<int:pk>", views.CartView.as_view(), name="edit_cart"),
    path("cart", views.CartView.as_view(), name="get_cart"),
    path("impressum", views.ImprintView.as_view(), name="imprint"),
    path("datenschutz", views.DataprotectionView.as_view(), name="dataprotection"),
]
