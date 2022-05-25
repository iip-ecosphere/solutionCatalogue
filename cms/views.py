from django.views import generic

from catalogue.utils import is_admin_or_mod
from .models import StaticMenuPage, BlogPage


class PageView(generic.DetailView):
    queryset = StaticMenuPage.objects.filter(published=True)
    template_name_field = "template"

    def get_queryset(self):
        if is_admin_or_mod(self.request):
            # allow preview for mods
            return StaticMenuPage.objects.all()
        else:
            return super().get_queryset()


class BlogList(generic.ListView):
    paginate_by = 5
    queryset = BlogPage.objects.filter(published=True)
    template_name = "blog/list.html"


class BlogDetail(generic.DetailView):
    queryset = BlogPage.objects.filter(published=True)
    context_object_name = "post"
    template_name = "blog/page.html"
