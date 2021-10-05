from django.contrib.auth.models import User
from django.db import models

from .component import Component


class SearchLog(models.Model):
    identifier = models.CharField("Identifier", max_length=100)
    query = models.CharField("Anfrage", max_length=5000, blank=True)
    created = models.DateTimeField("Erstellt", auto_now_add=True)

    class Meta:
        verbose_name = "Suchverlauf"
        verbose_name_plural = "Suchverläufe"

    def __str__(self):
        return "{}".format(self._meta.verbose_name)


class ComponentLog(models.Model):
    created = models.DateTimeField("Erstellt", auto_now_add=True)
    query = models.ForeignKey(
        SearchLog, on_delete=models.CASCADE, verbose_name="Suchanfrage"
    )
    component = models.ForeignKey(
        Component, on_delete=models.CASCADE, verbose_name="Lösung"
    )

    class Meta:
        verbose_name = "Besuchte Lösungen"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "{}".format(self._meta.verbose_name)
