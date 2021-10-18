from django.db import models
from django.conf import settings
from os import listdir
from os.path import isfile, join
from ckeditor.fields import RichTextField
from django.utils.functional import lazy


def load_template_choices():
    return [
        (f, f)
        for f in listdir(settings.CMS_TEMPLATE_DIR)
        if isfile(join(settings.CMS_TEMPLATE_DIR, f))
    ]


class BasePage(models.Model):
    title = models.CharField("Titel", max_length=100)
    template = models.CharField(
        "Template", max_length=100, choices=[("", "")], blank=False, default=None
    )
    content = RichTextField(blank=True)

    class Meta:
        abstract = True
        verbose_name = "Basis Seite"
        verbose_name_plural = verbose_name

    def __init__(self, *args, **kwargs):
        self._meta.get_field("template").choices = load_template_choices()
        super(BasePage, self).__init__(*args, **kwargs)


class Menu(models.Model):
    name = models.CharField("Name", max_length=15)

    class Meta:
        verbose_name = "Menü"
        verbose_name_plural = "Menüs"

    def __str__(self):
        return "{0}".format(self.name)


class StaticMenuPage(BasePage):
    menu = models.ForeignKey(
        Menu,
        on_delete=models.PROTECT,
        verbose_name="Menü",
    )
    root = models.BooleanField("Oberste Ebene", default=False)
    url = models.CharField(blank=True, max_length=200)
    parent = models.ForeignKey(
        "self",
        blank=True,
        limit_choices_to={"root": True},
        on_delete=models.PROTECT,
        verbose_name="Oberpunkt",
        null=True,
    )

    class Meta:
        verbose_name = "Menü Seiten"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "{0}".format(self.title)
