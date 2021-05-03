from django.db import models

from . import Component
from ..choices import TRLChoices, TaskChoices


class BaseData(models.Model):
    class Meta:
        verbose_name = "Grunddaten"
        verbose_name_plural = verbose_name

    component = models.OneToOneField(Component, on_delete=models.CASCADE)
    name = models.CharField(
        "Name",
        max_length=200,
        help_text="Bezeichnung der Komponente",
        blank=False,
        unique=True,
    )
    trl = models.IntegerField(
        "TRL",
        help_text=(
            "Status der Komponente in Bezug auf Ihre Einsetzbarkeit durch die Angabe"
            " eines Technischen Reifegrades (Technology Readiness Level)."
        ),
        choices=TRLChoices.choices,
    )
    description = models.TextField(
        "Kurzbeschreibung", help_text="Kurze Beschreibung der Komponente"
    )

    def __str__(self):
        return f"{self.name} - TRL {self.trl}"


class Task(models.Model):
    class Meta:
        verbose_name = "Task"
        verbose_name_plural = "Tasks"

    base_data = models.ForeignKey(BaseData, on_delete=models.CASCADE)
    name = models.CharField(
        choices=TaskChoices.choices,
        max_length=5,
        help_text=(
            "Art der Aufgabe, der die beschriebene KI-Komponente zugeordnet werden kann"
            " (z.B. Predictive Maintenance, Qualitätsprüfung))"
        ),
        blank=True,
    )

    def __str__(self):
        return self.get_name_display()
