from django.db import models
from django.contrib.auth.models import User

from ..choices import TRLChoices, RealtimeChoices


class BaseData(models.Model):
    class Meta:
        abstract = True
        verbose_name = "Grunddaten"
        verbose_name_plural = verbose_name

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


class ApplicationProfile(models.Model):
    class Meta:
        abstract = True
        verbose_name = "Anwendungsprofil"
        verbose_name_plural = verbose_name

    product = models.TextField("Produkt", help_text="Hergestelltes Produkt")

    def __str__(self):
        return self.product


class Use(models.Model):
    class Meta:
        abstract = True
        verbose_name = "Nutzen"
        verbose_name_plural = verbose_name

    scenarios = models.TextField(
        "Szenarien / Use cases",
        help_text="Beschreibung von Szenarien, in denen die Komponente bereits erfolgreich eingesetzt wurde",
    )

    def __str__(self):
        return self.scenarios


class Source(models.Model):
    class Meta:
        abstract = True
        verbose_name = "Quelle"
        verbose_name_plural = verbose_name

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

    def __str__(self):
        return ""


class TechnicalSpecification(models.Model):
    class Meta:
        abstract = True
        verbose_name = "Technische Spezifikation"
        verbose_name_plural = verbose_name

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

    def __str__(self):
        return ""


class Requirements(models.Model):
    class Meta:
        abstract = True
        verbose_name = "Vorraussetzungen"
        verbose_name_plural = verbose_name

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

    def __str__(self):
        return ""


class Component(ApplicationProfile, BaseData, Requirements, Source, Use, TechnicalSpecification):
    class Meta:
        verbose_name = "KI Komponente"
        verbose_name_plural = "KI Komponenten"

    created = models.DateTimeField("Erstellt", auto_now_add=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Erstellt von",
    )
    lastmodified_at = models.DateTimeField("Zuletzt bearbeitet", auto_now=True)
    published = models.BooleanField("Veröffentlicht", default=False)

    def __str__(self):
        return "{} {} - {}".format(self._meta.verbose_name, self.id, self.name)
