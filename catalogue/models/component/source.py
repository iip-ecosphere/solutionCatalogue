from django.db import models

from . import Component


class Source(models.Model):
    class Meta:
        verbose_name = "Quelle"
        verbose_name_plural = verbose_name

    component = models.OneToOneField(Component, on_delete=models.CASCADE)

    manufacturer = models.CharField(
        "Hersteller",
        help_text="Entwickler und/oder Hersteller der Komponente",
        max_length=1000,
    )
    contact = models.TextField(
        "Kontakt",
        help_text="Möglichkeit zum Hersteller Kontakt aufzunehmen",
        blank=True,
    )
    additional_info = models.TextField(
        "Zusatzinformationen", help_text="Zusatzinformation zur Komponente", blank=True
    )

    def __str__(self):
        return ""
