from django.views import generic
from django.shortcuts import render
from django.conf import settings
from django.shortcuts import get_object_or_404
from .models import StaticMenuPage, BlogPage
import pathlib


class PageView(generic.DetailView):
    model = StaticMenuPage
    context_object_name = "page"

    def get_template_names(self):
        return [pathlib.Path(__file__).parent / "templates" / self.object.template]


class BlogList(generic.ListView):
    paginate_by = 5
    queryset = BlogPage.objects.filter(published=True)
    context_object_name = "blog_posts"
    template_name = "blog/bloglist.html"


class BlogDetail(generic.DetailView):
    model = BlogPage
    context_object_name = "post"
    template_name = "blog/blogpage.html"
