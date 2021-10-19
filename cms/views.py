from django.views import generic
from django.shortcuts import render
from django.conf import settings
from django.shortcuts import get_object_or_404
from .models import StaticMenuPage


class PageView(generic.TemplateView):
    def get(self, request, page_url: str):
        self.page = get_object_or_404(StaticMenuPage, url=page_url)
        return render(
            request,
            settings.CMS_TEMPLATE_DIR / self.page.template,
            self.get_context_data(),
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context["page"] = self.page
        return context


class MenuView(generic.DetailView):
    pass
