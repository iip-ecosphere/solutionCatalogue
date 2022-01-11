from django.views import generic
from .models import StaticMenuPage, BlogPage


class PageView(generic.DetailView):
    queryset = StaticMenuPage.objects.filter(published=True)
    template_name_field = "template"


class BlogList(generic.ListView):
    paginate_by = 5
    queryset = BlogPage.objects.filter(published=True)
    template_name = "blog/list.html"


class BlogDetail(generic.DetailView):
    queryset = BlogPage.objects.filter(published=True)
    context_object_name = "post"
    template_name = "blog/page.html"
