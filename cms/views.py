from django.views import generic
from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponseRedirect
from .models import StaticMenuPage


class PageView(generic.TemplateView):
    def get(self, request, page_url: str):
        try:
            self.page = StaticMenuPage.objects.get(url=page_url)
            return render(
                request,
                settings.CMS_TEMPLATE_DIR / self.page.template,
                self.get_context_data(),
            )
        except StaticMenuPage.DoesNotExist:
            return HttpResponseRedirect("/")

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context["page"] = self.page
        return context


class MenuView(generic.DetailView):
    pass
