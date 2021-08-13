from django.db import models
from django.db.models.fields import URLField

from .users import User
from .component import Component


class SenderInfo(models.Model):
    class Meta:
        abstract = True

    created = models.DateTimeField("Erstellt", auto_now_add=True)
    name = models.CharField("Name", max_length=50)
    mail = models.EmailField("E-Mail-Adresse")


class Inquiry(SenderInfo):
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

    message = models.TextField(
        "Nachricht", help_text="Ihre Nachricht an den Anbieter", max_length=2000
    )

    def __str__(self):
        return "{} {}".format(self._meta.verbose_name, self.id)


class Feedback(SenderInfo):
    class Meta:
        verbose_name = "Feedback"
        verbose_name_plural = "Feedbacks"

    CHOICES = [("positive", "Positiv"), ("neutral", "Neutral"), ("negativ", "Negativ")]
    sentiment = models.CharField(
        "Wie zufieden sind Sie mit der Suche?",
        max_length=8,
        choices=CHOICES,
        default=CHOICES[0][0],
    )
    message = models.TextField("Nachricht", help_text="Ihr Feedback", max_length=2000)
    search_url = models.TextField(default=None)

    def __str__(self):
        return "{} {}".format(self._meta.verbose_name, self.id)


class Report(SenderInfo):
    class Meta:
        verbose_name = "Report"
        verbose_name_plural = "Report"

    component = models.ForeignKey(
        Component,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name=Component._meta.verbose_name,
    )

    message = models.TextField(
        "Warum möchten Sie diese Komponente melden?",
        help_text="Ihre Nachricht an die Admins",
        max_length=2000,
    )

    def __str__(self):
        return "{} {}".format(self._meta.verbose_name, self.id)
