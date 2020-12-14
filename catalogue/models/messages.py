from django.db import models

from .users import User
from .component import Component


class Inquiry(models.Model):
    class Meta:
        verbose_name = "Anfrage"
        verbose_name_plural = "Anfragen"

    recipient = models.ForeignKey(User, on_delete=models.CASCADE)
    component = models.ForeignKey(Component, on_delete=models.SET_NULL, null=True)
    name = models.CharField("Ihr Name", max_length=50)
    mail = models.CharField("Ihre E-Mail-Adresse", max_length=50)
    message = models.TextField("Nachricht", help_text="Ihre Nachricht an den Anbieter")
