from django.db import models

from ..choices import (
    CorporateDivisionChoices,
    HierarchyLevelChoices,
    ProcessChoices,
    BranchChoices,
)

from . import Component


class CorporateDivision(models.Model):
    class Meta:
        verbose_name = "Unternehmensbereich"
        verbose_name_plural = verbose_name

    component = models.ForeignKey(
        Component, on_delete=models.CASCADE
    )
    name = models.CharField(
        help_text="Bereich des produzierenden Unternehmens, für den die Komponenten entwickelt wurde",
        choices=CorporateDivisionChoices.choices,
        max_length=2,
        blank=True,
    )

    def __str__(self):
        return self.get_name_display()


class HierarchyLevel(models.Model):
    class Meta:
        verbose_name = "Hierarchie-Ebene"
        verbose_name_plural = verbose_name

    component = models.ForeignKey(
        Component, on_delete=models.CASCADE
    )
    name = models.CharField(
        choices=HierarchyLevelChoices.choices,
        help_text="Automatisierebene, für die die KI-Komponente gedacht ist",
        max_length=2,
        blank=True,
    )

    def __str__(self):
        return self.get_name_display()


class Process(models.Model):
    class Meta:
        verbose_name = "Prozess"
        verbose_name_plural = verbose_name

    component = models.ForeignKey(
        Component, on_delete=models.CASCADE
    )
    name = models.CharField(
        choices=ProcessChoices.choices,
        help_text="Prozess der durch die KI-Komponente unterstützt wird",
        max_length=5,
        blank=True,
    )

    def __str__(self):
        return self.get_name_display()


class BranchProven(models.Model):
    class Meta:
        verbose_name = "Branche (erprobt)"
        verbose_name_plural = verbose_name

    component = models.ForeignKey(
        Component, on_delete=models.CASCADE
    )
    name = models.CharField(
        help_text="Branche(n) für die die Komponente bereits erfolgreich erprobt wurde; belegte Anwendung",
        choices=BranchChoices.choices,
        max_length=3,
        blank=True,
    )

    def __str__(self):
        return self.get_name_display()


class BranchApplicable(models.Model):
    class Meta:
        verbose_name = "Branche (anwendbar)"
        verbose_name_plural = verbose_name

    component = models.ForeignKey(
        Component, on_delete=models.CASCADE
    )
    name = models.CharField(
        help_text="Branche, in denen die Komponenten anwendbar ist",
        choices=BranchChoices.choices,
        max_length=3,
        blank=True,
    )

    def __str__(self):
        return self.get_name_display()
