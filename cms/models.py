import pathlib
from typing import List, Tuple

from catalogue.models import Component
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


def load_template_choices() -> List[Tuple[str, str]]:
    return [
        (f.name, f.name)
        for f in (pathlib.Path(__file__).parent / "templates").iterdir()
        if f.is_file()
    ]


class BasePage(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Erstellt von",
        default=None,
    )
    created = models.DateTimeField("Erstellt", auto_now_add=True)
    title = models.CharField("Titel", max_length=100)
    slug = models.SlugField(default="", unique=True, max_length=200, verbose_name="URL")
    content = RichTextUploadingField(blank=True, config_name="cms")
    published = models.BooleanField(default=False, verbose_name="Veröffentlicht")

    class Meta:
        abstract = True


class Menu(models.Model):
    name = models.CharField("Name", max_length=15)

    class Meta:
        verbose_name = "Menü"
        verbose_name_plural = "Menüs"

    def __str__(self) -> str:
        return self.name


class StaticMenuPage(BasePage):
    menu = models.ForeignKey(
        Menu,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Menü",
    )
    template = models.CharField(
        "Template", max_length=100, choices=[("", "")], blank=False, default=None
    )
    root = models.BooleanField("Oberste Ebene", default=False)
    parent = models.ForeignKey(
        "self",
        blank=True,
        limit_choices_to={"root": True},
        on_delete=models.SET_NULL,
        verbose_name="Oberpunkt",
        null=True,
    )

    class Meta:
        verbose_name = "Seite"
        verbose_name_plural = "Seiten"

    def __init__(self, *args, **kwargs) -> None:
        self._meta.get_field("template").choices = load_template_choices()
        super(StaticMenuPage, self).__init__(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("cms:page", kwargs={"slug": self.slug})

    def __str__(self) -> str:
        return self.title


class BlogPage(BasePage):
    components = models.ManyToManyField(Component, blank=True, verbose_name="Lösungen")
    title_image = models.ImageField(
        upload_to="blog/", blank=True, verbose_name="Titelbild"
    )

    class Meta:
        verbose_name = "Blog Eintrag"
        verbose_name_plural = "Blog Einträge"
        ordering = ["-created"]

    def get_absolute_url(self):
        return reverse("cms:blog_page", kwargs={"slug": self.slug})

    def __str__(self) -> str:
        return self.title
