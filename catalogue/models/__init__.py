from django.db import models
from crum import get_current_user

from .choices import (
    TaskName,
    BranchName,
    DAProcessName,
    TRL,
    CorporateDivision,
    HierarchyLevel,
    Process,
    Realtime,
)
from .users import *


class Component(models.Model):
    class Meta:
        verbose_name = "KI Komponente"
        verbose_name_plural = "KI Komponenten"

    created = models.DateTimeField("Erstellt", auto_now_add=True)
    created_by = models.ForeignKey(
        "auth.User", default=get_current_user, on_delete=models.CASCADE
    )
    lastmodified_at = models.DateTimeField("Zuletzt bearbeitet", auto_now=True)
    published = models.BooleanField("Veröffentlicht", default=False)


class BaseData(models.Model):
    component = models.OneToOneField(Component, on_delete=models.CASCADE)
    name = models.CharField(
        "Name", max_length=200, help_text="Bezeichnung der Komponente", blank=False
    )
    trl = models.IntegerField(
        "TRL",
        help_text=(
            "Status der Komponente in Bezug auf Ihre Einsetzbarkeit durch die Angabe"
            " eines Technischen Reifegrades (Technology Readiness Level)."
        ),
        choices=TRL.choices,
    )
    description = models.TextField(
        "Kurzbeschreibung", help_text="Kurze Beschreibung der Komponente"
    )

    def __str__(self):
        return self.name


class Task(models.Model):
    class Meta:
        verbose_name = "Task"
        verbose_name_plural = "Tasks"

    base_data = models.ForeignKey(BaseData, on_delete=models.CASCADE)
    name = models.CharField(
        choices=TaskName.choices,
        max_length=5,
        help_text=(
            "Art der Aufgabe, der die beschriebene KI-Komponente zugeordnet werden kann"
            " (z.B. Predictive Maintenance, Qualitätsprüfung))"
        ),
    )

    def __str__(self):
        return self.get_name_display()


class ApplicationProfile(models.Model):
    component = models.OneToOneField(Component, on_delete=models.CASCADE)

    corporate_division = models.CharField(
        "Unternehmensbereich",
        choices=CorporateDivision.choices,
        help_text="Bereich des produzierenden Unternehmens, für den die Komponenten entwickelt wurde",
        max_length=2,
    )  # FIXME: Mehrfachauswahl?
    hierarchy_level = models.CharField(
        "Hierarchie-Ebene",
        choices=HierarchyLevel.choices,
        help_text="Automatisierebene, für die die KI-Komponente gedacht ist",
        max_length=2,
    )  # FIXME: Mehrfachauswahl?
    process = models.CharField(
        "Prozess",
        choices=Process.choices,
        help_text="Prozess der durch die KI-Komponente unterstützt wird",
        max_length=5,
    )  # FIXME: Mehrfachauswahl?
    product = models.TextField("Produkt", help_text="Hergestelltes Produkt")


class BranchProven(models.Model):
    class Meta:
        verbose_name = "Branche (erprobt)"

    application_profile = models.ForeignKey(
        ApplicationProfile, on_delete=models.CASCADE
    )
    name = models.CharField(
        help_text="Branche(n) für die die Komponente bereits erfolgreich erprobt wurde; belegte Anwendung",
        choices=BranchName.choices,
        max_length=3,
    )

    def __str__(self):
        return self.get_name_display()


class BranchApplicable(models.Model):
    class Meta:
        verbose_name = "Branche (anwendbar)"

    application_profile = models.ForeignKey(
        ApplicationProfile, on_delete=models.CASCADE
    )
    name = models.CharField(
        help_text="Branche, in denen die Komponenten anwendbar ist",
        choices=BranchName.choices,
        max_length=3,
    )

    def __str__(self):
        return self.get_name_display()


class Use(models.Model):
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


class Requirements(models.Model):
    component = models.OneToOneField(Component, on_delete=models.CASCADE)

    # FIXME: multiple inputs? max_length?
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


class TechnicalSpecification(models.Model):
    component = models.OneToOneField(Component, on_delete=models.CASCADE)

    ai_method = models.CharField(
        "KI-Methode",
        help_text="Angabe der verwendeten KI-Methode (z.B. Deep Learning)",
        max_length=1000,
        blank=True,
    )  # FIXME: multivalue? textfield?
    realtime_processing = models.IntegerField(
        "Echtzeitverarbeitung",
        help_text="Klassifizierung der Komponente in Bezug auf ihre Echtzeitfähigkeit",
        choices=Realtime.choices,
    )
    data_formats = models.CharField(
        "Datenformate",
        help_text="Datenformate, die von der KI-Komponente verarbeitet werden können und Datenformat der Ergebnisse",
        max_length=1000,
        blank=True,
    )
    licenses = models.CharField(
        "Lizenzen",
        help_text="Welche Lizenzen bringt die Komponente mit, insbesondere Open Source Lizenzen",
        max_length=1000,
        blank=True,
    )  # FIXME: multivalue? # TODO: choices

    # FIXME: planed for later
    # machine_readable_spec = models.CharField("Maschinenlesbare Spezifikation",
    # help_text="Beschreibung der Schnittstellen in maschinenlesbarer Form, um automatische Integration zu unterstützen")


class DataAnalysisProcess(models.Model):
    class Meta:
        verbose_name = "Datenanalyse-Prozess"

    technical_specification = models.ForeignKey(
        TechnicalSpecification, on_delete=models.CASCADE
    )
    name = models.CharField(
        choices=DAProcessName.choices,
        max_length=2,
        help_text="Unterstützte Phasen des Datenanalyse-Prozesses (z.B. Data Cleaning)",
    )

    # FIXME: "einzelne Schritte des Prozesses erklären"?

    def __str__(self):
        return self.get_name_display()


class Source(models.Model):
    component = models.OneToOneField(Component, on_delete=models.CASCADE)

    developer = models.CharField(
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
