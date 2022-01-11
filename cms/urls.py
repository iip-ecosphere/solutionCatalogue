from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = "cms"

urlpatterns = [
    path("blog/<slug:slug>", views.BlogDetail.as_view(), name="blog_page"),
    path("blog", views.BlogList.as_view(), name="blog"),
    path("<slug:slug>", views.PageView.as_view(), name="page"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
