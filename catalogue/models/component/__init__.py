from django.db import models
from django.contrib.auth.models import User


class Component(models.Model):
    class Meta:
        verbose_name = "KI Komponente"
        verbose_name_plural = "KI Komponenten"

    created = models.DateTimeField("Erstellt", auto_now_add=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Erstellt von",
    )
    lastmodified_at = models.DateTimeField("Zuletzt bearbeitet", auto_now=True)
    published = models.BooleanField("Veröffentlicht", default=False)

    def __str__(self):
        return "{} {} - {}".format(self._meta.verbose_name, self.id, self.basedata.name)
