from django.db import models

from . import Component
from ..choices import DAProcessChoices, LicenseChoices


class AIMethod(models.Model):
    component = models.ForeignKey(Component, on_delete=models.CASCADE)
    name = models.CharField(
        help_text="Angabe der verwendeten KI-Methode (z.B. Deep Learning)",
        max_length=1000,
        blank=True,
    )

    class Meta:
        verbose_name = "KI-Methode"
        verbose_name_plural = verbose_name

    def __str__(self) -> str:
        return self.name


class DataAnalysisProcess(models.Model):
    component = models.ForeignKey(Component, on_delete=models.CASCADE)
    name = models.CharField(
        choices=DAProcessChoices.choices,
        max_length=2,
        help_text="Unterstützte Phasen des Datenanalyse-Prozesses (z.B. Data Cleaning)",
        blank=True,
    )

    # FIXME: "einzelne Schritte des Prozesses erklären"

    class Meta:
        verbose_name = "Datenanalyse-Prozess"
        verbose_name_plural = verbose_name

    def __str__(self) -> str:
        return self.get_name_display()


class Licenses(models.Model):
    component = models.ForeignKey(Component, on_delete=models.CASCADE)
    type = models.CharField(
        "Typ",
        choices=LicenseChoices.choices,
        max_length=4,
        help_text="Welche Lizenzen bringt die Lösung mit, insbesondere Open Source Lizenzen",
        blank=True,
    )
    name = models.CharField(
        help_text="Genaue Angabe der Lizenz",
        max_length=1000,
        blank=True,
    )

    class Meta:
        verbose_name = "Lizenz"
        verbose_name_plural = "Lizenzen"

    def __str__(self) -> str:
        if self.name:
            return f"{self.get_type_display()} - {self.name}"
        else:
            return f"{self.get_type_display()}"
