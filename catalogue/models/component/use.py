from django.db import models

from . import Component


class Use(models.Model):
    class Meta:
        verbose_name = "Nutzen"
        verbose_name_plural = verbose_name

    component = models.OneToOneField(Component, on_delete=models.CASCADE)
    kpi = models.CharField(
        "KPI",
        help_text=(
            "Key Performance Indikator, der durch die Komponente optimiert werden soll;"
            "es sollte auf jeden Fall eine Kategorie ausgesucht werden (Wert);"
            " dies Auswahl kann über KPI-Verfeinerung noch verfeinert werden;"
        ),
        max_length=1000,
    )  # TODO: Hierarchy
    scenarios = models.TextField(
        "Szenarien / Use cases",
        help_text="Beschreibung von Szenarien, in denen die Komponente bereits erfolgreich eingesetzt wurde",
    )

    def __str__(self):
        return ""
