from django.db import models

from ..choices import (
    CorporateDivisionChoices,
    HierarchyLevelChoices,
    ProcessChoices,
    BranchChoices,
)

from . import Component


class CorporateDivision(models.Model):
    component = models.ForeignKey(Component, on_delete=models.CASCADE)
    name = models.CharField(
        help_text="Bereich des produzierenden Unternehmens, für den die Lösungen entwickelt wurde",
        choices=CorporateDivisionChoices.choices,
        max_length=2,
        blank=True,
    )

    class Meta:
        verbose_name = "Unternehmensbereich"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.get_name_display()


class HierarchyLevel(models.Model):
    component = models.ForeignKey(Component, on_delete=models.CASCADE)
    name = models.CharField(
        choices=HierarchyLevelChoices.choices,
        help_text="Automatisierebene, für die die KI-Lösung gedacht ist",
        max_length=2,
        blank=True,
    )

    class Meta:
        verbose_name = "Hierarchie-Ebene"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.get_name_display()


class Process(models.Model):
    component = models.ForeignKey(Component, on_delete=models.CASCADE)
    name = models.CharField(
        choices=ProcessChoices.choices,
        help_text="Prozess der durch die KI-Lösung unterstützt wird",
        max_length=5,
        blank=True,
    )

    class Meta:
        verbose_name = "Prozess"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.get_name_display()


class BranchProven(models.Model):
    component = models.ForeignKey(Component, on_delete=models.CASCADE)
    name = models.CharField(
        help_text="Branche(n) für die die Lösung bereits erfolgreich erprobt wurde; belegte Anwendung",
        choices=BranchChoices.choices,
        max_length=3,
        blank=True,
    )

    class Meta:
        verbose_name = "Branche (erprobt)"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.get_name_display()


class BranchApplicable(models.Model):
    component = models.ForeignKey(Component, on_delete=models.CASCADE)
    name = models.CharField(
        help_text="Branche, in denen die Lösungen anwendbar ist",
        choices=BranchChoices.choices,
        max_length=3,
        blank=True,
    )

    class Meta:
        verbose_name = "Branche (anwendbar)"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.get_name_display()
