from django.db import models

from .users import User
from .component import Component


class SenderInfo(models.Model):
    created = models.DateTimeField("Erstellt", auto_now_add=True)
    name = models.CharField("Name", max_length=50)
    mail = models.EmailField("E-Mail-Adresse")

    class Meta:
        abstract = True


class Inquiry(SenderInfo):
    recipient = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Adressat"
    )
    component = models.ForeignKey(
        Component,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name=Component._meta.verbose_name,
    )
    message = models.TextField(
        "Nachricht", help_text="Ihre Nachricht an den Anbieter", max_length=2000
    )

    class Meta:
        verbose_name = "Anfrage"
        verbose_name_plural = "Anfragen"

    def __str__(self):
        return "{} {}".format(self._meta.verbose_name, self.id)


class Feedback(SenderInfo):
    CHOICES = [("positive", "Positiv"), ("neutral", "Neutral"), ("negativ", "Negativ")]
    sentiment = models.CharField(
        "Wie zufieden sind Sie mit der Suche?",
        max_length=8,
        choices=CHOICES,
        default=CHOICES[0][0],
    )
    message = models.TextField("Nachricht", help_text="Ihr Feedback", max_length=2000)
    search_url = models.TextField("Such-URL", default=None)

    class Meta:
        verbose_name = "Such-Feedback"
        verbose_name_plural = "Such-Feedback"

    def __str__(self):
        return "{} {}".format(self._meta.verbose_name, self.id)


class Report(SenderInfo):
    component = models.ForeignKey(
        Component,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name=Component._meta.verbose_name,
    )
    message = models.TextField(
        "Warum möchten Sie diese Komponente melden?",
        help_text="Ihre Nachricht",
        max_length=2000,
    )

    class Meta:
        verbose_name = "Meldung"
        verbose_name_plural = "Meldungen"

    def __str__(self):
        return "{} {}".format(self._meta.verbose_name, self.id)
