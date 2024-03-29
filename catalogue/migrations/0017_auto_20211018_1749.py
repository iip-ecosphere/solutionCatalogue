# Generated by Django 3.2.7 on 2021-10-18 15:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0016_alter_component_protocols'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='task',
            options={'verbose_name': 'Aufgabe', 'verbose_name_plural': 'Aufgaben'},
        ),
        migrations.AlterField(
            model_name='task',
            name='name',
            field=models.CharField(blank=True, choices=[(None, 'Bitte Wert auswählen'), ('PMCM', 'Predictive Maintenance/Condition Monitoring'), ('QCM', 'Qualitätskontrolle und –management'), ('OPP', 'Optimierte Prozessplanung'), ('OPC', 'Optimierte Prozesssteuerung'), ('RAS', 'Robotik & autonome Systeme'), ('IST', 'Intelligente Sensorik'), ('KM', 'Wissensmanagement'), ('FPA', 'Vorhersagen und Predictive Analytics'), ('ORS', 'Optimiertes Ressourcenmanagement'), ('IA', 'Intelligente Automatisierung'), ('IAS', 'Intelligente Assistenzsysteme'), ('DA', 'Datenanalyse'), ('DM', 'Data Management'), ('VAR', 'Virtuelle und erweiterte Realität'), ('OTHER', 'Sonstiges')], help_text='Art der Aufgabe, der die beschriebene KI-Lösung zugeordnet werden kann (z.B. Predictive Maintenance, Qualitätsprüfung)', max_length=5),
        ),
    ]
