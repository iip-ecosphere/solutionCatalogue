# Generated by Django 3.2.4 on 2021-08-13 12:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0006_component_allow_email'),
    ]

    operations = [
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Erstellt')),
                ('name', models.CharField(max_length=50, verbose_name='Name')),
                ('mail', models.EmailField(max_length=254, verbose_name='E-Mail-Adresse')),
                ('message', models.TextField(help_text='Ihre Nachricht', max_length=2000, verbose_name='Warum möchten Sie diese Komponente melden?')),
                ('component', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='catalogue.component', verbose_name='KI Lösung')),
            ],
            options={
                'verbose_name': 'Meldung',
                'verbose_name_plural': 'Meldungen',
            },
        ),
    ]
