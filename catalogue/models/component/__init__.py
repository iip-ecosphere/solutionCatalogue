import os
import uuid
from typing import List, Tuple
from pathlib import Path

from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.validators import RegexValidator
from ckeditor.fields import RichTextField
from django.core.exceptions import ValidationError
from PIL import Image

from ..choices import TRLChoices, RealtimeChoices


def get_file_path(instance, filename: str) -> Path:
    return Path("component_uploads") / str(instance.id) / filename


def get_image_path(instance, filename):
    ext = filename.split(".")[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join("component_uploads/", filename)


def validate_image_size(image):
    MIN_WIDTH = 1153
    MIN_HEIGHT = 0
    img = Image.open(image)
    fw, fh = img.size
    if fw < MIN_WIDTH or fh < MIN_HEIGHT:
        raise ValidationError("Das Bild muss mindestens 1153px breit sein!")


class BaseData(models.Model):
    name = models.CharField(
        "Name",
        max_length=200,
        help_text="Bezeichnung der Lösung",
        blank=False,
        unique=True,
    )
    trl = models.IntegerField(
        "TRL",
        help_text=(
            "Status der Lösung in Bezug auf Ihre Einsetzbarkeit durch die Angabe"
            " eines technischen Reifegrades (Technology Readiness Level)."
        ),
        choices=TRLChoices.choices,
    )
    description = models.TextField(
        "Kurzbeschreibung", help_text="Kurze Beschreibung der Lösung", max_length=1000
    )
    url = models.URLField("URL", help_text="Öffentlicher Link zur Lösung", blank=True)
    image = models.ImageField(
        "Titelbild",
        upload_to=get_image_path,
        help_text="Titelbild der Lösung",
        blank=True,
        validators=[validate_image_size],
    )

    class Meta:
        abstract = True
        verbose_name = "Grunddaten"
        verbose_name_plural = verbose_name


class ApplicationProfile(models.Model):
    long_description = RichTextField(
        "Beschreibung",
        help_text="Ausführliche Beschreibung der Lösung",
        config_name="component",
    )

    class Meta:
        abstract = True
        verbose_name = "Anwendungsprofil"
        verbose_name_plural = verbose_name


class Use(models.Model):
    scenarios = RichTextField(
        "Szenarien / Use cases",
        help_text="Beschreibung von Szenarien, in denen die Lösung bereits erfolgreich eingesetzt wurde",
        config_name="component",
    )

    class Meta:
        abstract = True
        verbose_name = "Nutzen"
        verbose_name_plural = verbose_name


class TechnicalSpecification(models.Model):
    realtime_processing = models.IntegerField(
        "Echtzeitverarbeitung",
        help_text="Klassifizierung der Lösung in Bezug auf ihre Echtzeitfähigkeit",
        choices=RealtimeChoices.choices,
    )
    data_formats = models.CharField(
        "Datenformate",
        help_text="Datenformate, die von der KI-Lösung verarbeitet werden können und Datenformat der Ergebnisse",
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


class Requirements(models.Model):
    protocols = models.CharField(
        "Protokolle / Schnittstellen",
        help_text="Schnittstellen und/oder Protokolle, die von der Lösung unterstützt werden",
        max_length=1000,
    )
    it_environment = models.CharField(
        "IT Umgebung / Software",
        help_text=(
            "Anforderungen an die IT-Umgebung (inkl. IT Hardware) und an weitere Software/Bibliotheken"
            ", die für den Betrieb der Lösung notwendig sind"
        ),
        max_length=1000,
    )
    hardware_requirements = models.CharField(
        "Spezielle Hardware",
        help_text="Spezielle Hardware, welche für den Betrieb der Lösung notwendig ist (z.B. Kamera, Roboter)",
        max_length=1000,
    )
    devices = models.CharField(
        "Maschinen / Steuerungen",
        help_text="Maschinen und IoT Devices, mit denen die Lösung kompatibel ist",
        max_length=1000,
    )

    class Meta:
        abstract = True
        verbose_name = "Vorraussetzungen"
        verbose_name_plural = verbose_name


class Contact(models.Model):
    # Contact Information
    contact_manufacturer = models.CharField(
        "Hersteller",
        help_text="Entwickler und/oder Hersteller der Lösung",
        max_length=1000,
    )
    contact_person_name = models.CharField(
        "Name",
        help_text="Name des zuständigen Mitarbeiters",
        max_length=100,
    )
    contact_email = models.EmailField(
        "Email",
        help_text="Email Adresse des zuständigen Mitarbeiters",
        max_length=100,
    )
    contact_phone = models.CharField(
        "Telefonnummer",
        help_text="Telefonnummer des zuständigen Mitarbeiters",
        max_length=17,
        validators=[
            RegexValidator(
                regex=r"^\+?1?\d{9,15}$",
                message="Die Telefonnummer muss folgendes Format ausweisen: '+999999999'.",
            )
        ],
        blank=True,
    )
    contact_address_street = models.CharField(
        "Straße",
        help_text="Straße des Anbieters",
        max_length=100,
        blank=True,
    )
    contact_address_city = models.CharField(
        "Stadt",
        help_text="Stadt in der sich der Anbieter befindet",
        max_length=100,
        blank=True,
    )
    contact_address_zip = models.CharField(
        "PLZ",
        help_text="PLZ in der sich der Anbieter befindet",
        max_length=10,
        blank=True,
    )
    contact_address_country = models.CharField(
        "Land",
        help_text="Land in dem sich der Anbieter befindet",
        max_length=100,
        default="Deutschland",
    )
    contact_additional_info = models.TextField(
        "Zusatzinformationen", help_text="Zusatzinformation zur Lösung", blank=True
    )

    class Meta:
        abstract = True
        verbose_name = "Kontakt Informationen"
        verbose_name_plural = verbose_name


class PublicComponentManager(models.Manager):
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(approved=True)
            .filter(published=True)
            .filter(is_deleted=False)
        )


class Component(
    ApplicationProfile,
    BaseData,
    Requirements,
    Use,
    TechnicalSpecification,
    Contact,
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
    published = models.BooleanField(
        "Veröffentlicht",
        help_text=(
            "Lösung bereit zur Veröffentlichung. "
            "Nach anschließender Moderation wird Ihre Lösung öffentlich zugänglich."
        ),
        default=False,
    )
    allow_email = models.BooleanField(
        "Erlaube Kontaktaufnahme per Mail",
        help_text="Erlaubt die Einblendung eines Kontaktformulares.",
        default=True,
    )
    approved = models.BooleanField(
        "Freigegeben",
        help_text="Lösung wird nach Moderation freigegeben",
        default=False,
    )
    frontpage = models.BooleanField("Auf der Startseite anzeigen?", default=False)
    is_deleted = models.BooleanField("Gelöscht", default=False)

    class Meta:
        verbose_name = "KI Lösung"
        verbose_name_plural = "KI Lösungen"

    def __str__(self) -> str:
        return f"{self._meta.verbose_name} {self.id} - {self.name}"

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

    def get_contact(self) -> Tuple[str, List[str]]:
        return Contact._meta.verbose_name, [x.name for x in Contact._meta.get_fields()]

    def get_absolute_url(self):
        return reverse("catalogue:detail", kwargs={"pk": self.pk})


class ComponentFile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    component = models.ForeignKey(Component, on_delete=models.CASCADE)
    file = models.FileField("Datei", upload_to=get_file_path, blank=True)

    class Meta:
        verbose_name = "Dokument"
        verbose_name_plural = "Dokumente"

    def __str__(self) -> str:
        return f"{self._meta.verbose_name} {self.id} - {self.filename}"

    @property
    def filename(self) -> str:
        return Path(self.file.name).name

    def get_absolute_url(self):
        return reverse("catalogue:component_document_download", kwargs={"id": self.id})
