from django.db import models

from . import Component
from ..choices import Realtime, DAProcessName


class TechnicalSpecification(models.Model):
    class Meta:
        verbose_name = "Technische Spezifikation"
        verbose_name_plural = verbose_name

    component = models.OneToOneField(Component, on_delete=models.CASCADE)

    realtime_processing = models.IntegerField(
        "Echtzeitverarbeitung",
        help_text="Klassifizierung der Komponente in Bezug auf ihre Echtzeitfähigkeit",
        choices=Realtime.choices,
    )
    data_formats = models.CharField(
        "Datenformate",
        help_text="Datenformate, die von der KI-Komponente verarbeitet werden können und Datenformat der Ergebnisse",
        max_length=1000,
        blank=True,
    )
    licenses = models.CharField(
        "Lizenzen",
        help_text="Welche Lizenzen bringt die Komponente mit, insbesondere Open Source Lizenzen",
        max_length=1000,
        blank=True,
    )  # FIXME: multivalue? # TODO: choices

    # FIXME: planed for later
    # machine_readable_spec = models.CharField("Maschinenlesbare Spezifikation",
    # help_text="Beschreibung der Schnittstellen in maschinenlesbarer Form, um automatische Integration zu unterstützen")

    def __str__(self):
        return ""


class AIMethod(models.Model):
    class Meta:
        verbose_name = "KI-Methode"
        verbose_name_plural = verbose_name

    technical_specification = models.ForeignKey(
        TechnicalSpecification, on_delete=models.CASCADE
    )
    name = models.CharField(
        help_text="Angabe der verwendeten KI-Methode (z.B. Deep Learning)",
        max_length=1000,
        blank=True,
    )

    def __str__(self):
        return ""


class DataAnalysisProcess(models.Model):
    class Meta:
        verbose_name = "Datenanalyse-Prozess"
        verbose_name_plural = verbose_name

    technical_specification = models.ForeignKey(
        TechnicalSpecification, on_delete=models.CASCADE
    )
    name = models.CharField(
        choices=DAProcessName.choices,
        max_length=2,
        help_text="Unterstützte Phasen des Datenanalyse-Prozesses (z.B. Data Cleaning)",
        blank=True,
    )

    # FIXME: "einzelne Schritte des Prozesses erklären"?

    def __str__(self):
        return ""
