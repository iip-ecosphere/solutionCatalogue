# Generated by Django 3.2.4 on 2021-09-06 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0008_component_approved'),
    ]

    operations = [
        migrations.AddField(
            model_name='component',
            name='frontpage',
            field=models.BooleanField(default=False, verbose_name='Auf der Startseite anzeigen?'),
        ),
    ]
