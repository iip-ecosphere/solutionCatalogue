from django.db import models

from ..choices import KPIChoices

from . import Component


class KPI(models.Model):
    component = models.ForeignKey(Component, on_delete=models.CASCADE)
    # TODO: Hierarchy
    type = models.CharField(
        "Typ",
        choices=KPIChoices.choices,
        max_length=3,
        help_text=(
            "Key Performance Indikator, der durch die Lösung optimiert werden soll;"
            "es sollte auf jeden Fall eine Kategorie ausgesucht werden (Wert);"
            " dies Auswahl kann über KPI-Verfeinerung noch verfeinert werden;"
        ),
        blank=True,
    )

    class Meta:
        verbose_name = "KPI"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.get_type_display()
