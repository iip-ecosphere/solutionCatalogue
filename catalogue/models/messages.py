from django.db import models

from .users import User
from .component import Component


class Inquiry(models.Model):
    class Meta:
        verbose_name = "Anfrage"
        verbose_name_plural = "Anfragen"

    recipient = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Adressat"
    )
    component = models.ForeignKey(
        Component,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name=Component._meta.verbose_name,
    )
    created = models.DateTimeField("Erstellt", auto_now_add=True)
    name = models.CharField("Name", max_length=50)
    mail = models.EmailField("E-Mail-Adresse")
    message = models.TextField(
        "Nachricht", help_text="Ihre Nachricht an den Anbieter", max_length=2000
    )

    def __str__(self):
        return "{} {}".format(self._meta.verbose_name, self.id)
