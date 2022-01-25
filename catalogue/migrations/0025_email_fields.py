# Generated by Django 3.2.11 on 2022-01-25 16:45

from django.db import migrations, models


def move_values(apps, schema_editor):
    Component = apps.get_model('catalogue', 'component')
    for c in Component.objects.all():
        c.contact_email_form = c.allow_email
        c.save()


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0024_component_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='component',
            name='contact_email_form',
            field=models.BooleanField(default=True,
                                      help_text='Erlaubt die Einblendung eines Kontaktformulares. Nachricht wird an die angegebene Email Adresse gesendet.',
                                      verbose_name='Kontaktformular'),
        ),
        migrations.AddField(
            model_name='component',
            name='contact_email_show',
            field=models.BooleanField(default=True, help_text='Zeigt die Email öffentlich an.',
                                      verbose_name='Email Adresse öffentlich'),
        ),
        migrations.RunPython(move_values),
        migrations.RemoveField(
            model_name='component',
            name='allow_email',
        ),
    ]
