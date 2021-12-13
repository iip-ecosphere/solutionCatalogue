from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = "cms"

urlpatterns = [
    path("<slug:slug>", views.PageView.as_view(), name="page"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
