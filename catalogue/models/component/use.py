from django.db import models

from . import Component
from ..choices import KPIChoices


class Use(models.Model):
    class Meta:
        verbose_name = "Nutzen"
        verbose_name_plural = verbose_name

    component = models.OneToOneField(Component, on_delete=models.CASCADE)
    scenarios = models.TextField(
        "Szenarien / Use cases",
        help_text="Beschreibung von Szenarien, in denen die Komponente bereits erfolgreich eingesetzt wurde",
    )

    def __str__(self):
        return self.scenarios


class KPI(models.Model):
    class Meta:
        verbose_name = "KPI"
        verbose_name_plural = verbose_name

    technical_specification = models.ForeignKey(Use, on_delete=models.CASCADE)
    # TODO: Hierarchy
    type = models.CharField(
        "Typ",
        choices=KPIChoices.choices,
        max_length=3,
        help_text=(
            "Key Performance Indikator, der durch die Komponente optimiert werden soll;"
            "es sollte auf jeden Fall eine Kategorie ausgesucht werden (Wert);"
            " dies Auswahl kann über KPI-Verfeinerung noch verfeinert werden;"
        ),
        blank=True,
    )

    def __str__(self):
        return self.get_type_display()
