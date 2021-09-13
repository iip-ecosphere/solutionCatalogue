from django.db import models

from . import Component
from ..choices import TaskChoices


class Task(models.Model):
    component = models.ForeignKey(Component, on_delete=models.CASCADE)
    name = models.CharField(
        choices=TaskChoices.choices,
        max_length=5,
        help_text=(
            "Art der Aufgabe, der die beschriebene KI-Komponente zugeordnet werden kann"
            " (z.B. Predictive Maintenance, Qualitätsprüfung))"
        ),
        blank=True,
    )

    class Meta:
        verbose_name = "Task"
        verbose_name_plural = "Tasks"

    def __str__(self):
        return self.get_name_display()
