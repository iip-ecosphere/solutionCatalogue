from django.db import models

from . import Component


class Requirements(models.Model):
    class Meta:
        verbose_name = "Vorraussetzungen"
        verbose_name_plural = verbose_name

    component = models.OneToOneField(Component, on_delete=models.CASCADE)

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
