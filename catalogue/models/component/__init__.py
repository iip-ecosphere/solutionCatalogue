from typing import List, Tuple

from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

from ..choices import TRLChoices, RealtimeChoices


class BaseData(models.Model):
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

    class Meta:
        abstract = True
        verbose_name = "Grunddaten"
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.name} - TRL {self.trl}"


class ApplicationProfile(models.Model):
    product = models.TextField("Produkt", help_text="Hergestelltes Produkt")

    class Meta:
        abstract = True
        verbose_name = "Anwendungsprofil"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.product


class Use(models.Model):
    scenarios = models.TextField(
        "Szenarien / Use cases",
        help_text="Beschreibung von Szenarien, in denen die Komponente bereits erfolgreich eingesetzt wurde",
    )

    class Meta:
        abstract = True
        verbose_name = "Nutzen"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.scenarios


class Source(models.Model):
    manufacturer = models.CharField(
        "Hersteller",
        help_text="Entwickler und/oder Hersteller der Komponente",
        max_length=1000,
    )
    contact = models.TextField(
        "Kontakt",
        help_text="Möglichkeit zum Hersteller Kontakt aufzunehmen",
        blank=True,
    )
    additional_info = models.TextField(
        "Zusatzinformationen", help_text="Zusatzinformation zur Komponente", blank=True
    )

    class Meta:
        abstract = True
        verbose_name = "Quelle"
        verbose_name_plural = verbose_name

    def __str__(self):
        return ""


class TechnicalSpecification(models.Model):
    realtime_processing = models.IntegerField(
        "Echtzeitverarbeitung",
        help_text="Klassifizierung der Komponente in Bezug auf ihre Echtzeitfähigkeit",
        choices=RealtimeChoices.choices,
    )
    data_formats = models.CharField(
        "Datenformate",
        help_text="Datenformate, die von der KI-Komponente verarbeitet werden können und Datenformat der Ergebnisse",
        max_length=1000,
        blank=True,
    )

    # FIXME: planed for later
    # machine_readable_spec = models.CharField("Maschinenlesbare Spezifikation",
    # help_text="Beschreibung der Schnittstellen in maschinenlesbarer Form, um automatische Integration zu unterstützen")

    class Meta:
        abstract = True
        verbose_name = "Technische Spezifikation"
        verbose_name_plural = verbose_name

    def __str__(self):
        return ""


class Requirements(models.Model):
    protocols = models.CharField(
        "Protokolle/Schnittstellen",
        help_text="Schnittstellen und/oder Protokolle, die von der Kompomente unterstützt werden",
        max_length=1000,
    )
    it_environment = models.CharField(
        "IT Umgebung/Software",
        help_text=(
            "Anforderungen an die IT-Umgebung (inkl. IT Hardware) und an weitere Software/Bibliotheken"
            ", die für den Betrieb der Komponente notwendig sind"
        ),
        max_length=1000,
    )
    hardware_requirements = models.CharField(
        "Spezielle Hardware",
        help_text="Spezielle Hardware, welche für den Betrieb der Komponente notwendig ist (z.B. Kamera, Roboter)",
        max_length=1000,
    )
    devices = models.CharField(
        "Maschinen/Steuerungen",
        help_text="Maschinen und IoT Devices, mit denen die Komponente kompatibel ist",
        max_length=1000,
    )

    class Meta:
        abstract = True
        verbose_name = "Vorraussetzungen"
        verbose_name_plural = verbose_name

    def __str__(self):
        return ""


class PublicComponentManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(approved=True).filter(published=True)


class Component(
    ApplicationProfile, BaseData, Requirements, Source, Use, TechnicalSpecification
):
    objects = models.Manager()
    public_objects = PublicComponentManager()

    created = models.DateTimeField("Erstellt", auto_now_add=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Erstellt von",
    )
    lastmodified_at = models.DateTimeField("Zuletzt bearbeitet", auto_now=True)
    published = models.BooleanField("Veröffentlicht", default=False)
    allow_email = models.BooleanField("Erlaube Kontaktaufnahme per Mail", default=True)
    approved = models.BooleanField("Freigegeben", default=False)
    frontpage = models.BooleanField("Auf der Startseite anzeigen?", default=False)

    class Meta:
        verbose_name = "KI Lösung"
        verbose_name_plural = "KI Lösungen"

    def __str__(self) -> str:
        return "{} {} - {}".format(self._meta.verbose_name, self.id, self.name)

    def get_basedata(self) -> Tuple[str, List[str]]:
        return (
            BaseData._meta.verbose_name,
            [x.name for x in BaseData._meta.get_fields()] + ["task"],
        )

    def get_application_profile(self) -> Tuple[str, List[str]]:
        return ApplicationProfile._meta.verbose_name, [
            x.name for x in ApplicationProfile._meta.get_fields()
        ] + [
            "corporatedivision",
            "hierarchylevel",
            "process",
            "branchproven",
            "branchapplicable",
        ]

    def get_use(self) -> Tuple[str, List[str]]:
        return Use._meta.verbose_name, [x.name for x in Use._meta.get_fields()] + [
            "kpi"
        ]

    def get_requirements(self) -> Tuple[str, List[str]]:
        return Requirements._meta.verbose_name, [
            x.name for x in Requirements._meta.get_fields()
        ]

    def get_technical_specification(self) -> Tuple[str, List[str]]:
        return (
            TechnicalSpecification._meta.verbose_name,
            [x.name for x in TechnicalSpecification._meta.get_fields()]
            + ["aimethod", "dataanalysisprocess", "licenses"],
        )

    def get_source(self) -> Tuple[str, List[str]]:
        return Source._meta.verbose_name, [x.name for x in Source._meta.get_fields()]

    def get_absolute_url(self):
        return reverse("catalogue:detail", kwargs={"pk": self.pk})
