from django.db import models

from . import Component
from ..choices import (
    CorporateDivisionChoices,
    HierarchyLevelChoices,
    ProcessChoices,
    BranchChoices,
)


class ApplicationProfile(models.Model):
    class Meta:
        verbose_name = "Anwendungsprofil"
        verbose_name_plural = verbose_name

    component = models.OneToOneField(Component, on_delete=models.CASCADE)
    product = models.TextField("Produkt", help_text="Hergestelltes Produkt")

    def __str__(self):
        return ""


class CorporateDivision(models.Model):
    class Meta:
        verbose_name = "Unternehmensbereich"
        verbose_name_plural = verbose_name

    application_profile = models.ForeignKey(
        ApplicationProfile, on_delete=models.CASCADE
    )
    name = models.CharField(
        help_text="Bereich des produzierenden Unternehmens, für den die Komponenten entwickelt wurde",
        choices=CorporateDivisionChoices.choices,
        max_length=2,
        blank=True,
    )

    def __str__(self):
        return ""


class HierarchyLevel(models.Model):
    class Meta:
        verbose_name = "Hierarchie-Ebene"
        verbose_name_plural = verbose_name

    application_profile = models.ForeignKey(
        ApplicationProfile, on_delete=models.CASCADE
    )
    name = models.CharField(
        choices=HierarchyLevelChoices.choices,
        help_text="Automatisierebene, für die die KI-Komponente gedacht ist",
        max_length=2,
        blank=True,
    )

    def __str__(self):
        return ""


class Process(models.Model):
    class Meta:
        verbose_name = "Prozess"
        verbose_name_plural = verbose_name

    application_profile = models.ForeignKey(
        ApplicationProfile, on_delete=models.CASCADE
    )
    name = models.CharField(
        choices=ProcessChoices.choices,
        help_text="Prozess der durch die KI-Komponente unterstützt wird",
        max_length=5,
        blank=True,
    )

    def __str__(self):
        return ""


class BranchProven(models.Model):
    class Meta:
        verbose_name = "Branche (erprobt)"
        verbose_name_plural = verbose_name

    application_profile = models.ForeignKey(
        ApplicationProfile, on_delete=models.CASCADE
    )
    name = models.CharField(
        help_text="Branche(n) für die die Komponente bereits erfolgreich erprobt wurde; belegte Anwendung",
        choices=BranchChoices.choices,
        max_length=3,
        blank=True,
    )

    def __str__(self):
        return ""


class BranchApplicable(models.Model):
    class Meta:
        verbose_name = "Branche (anwendbar)"
        verbose_name_plural = verbose_name

    application_profile = models.ForeignKey(
        ApplicationProfile, on_delete=models.CASCADE
    )
    name = models.CharField(
        help_text="Branche, in denen die Komponenten anwendbar ist",
        choices=BranchChoices.choices,
        max_length=3,
        blank=True,
    )

    def __str__(self):
        return ""
