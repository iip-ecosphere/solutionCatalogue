# Generated by Django 3.2.4 on 2021-06-12 13:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0004_auto_20210604_1450'),
    ]

    operations = [
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Erstellt')),
                ('name', models.CharField(max_length=50, verbose_name='Name')),
                ('mail', models.EmailField(max_length=254, verbose_name='E-Mail-Adresse')),
                ('message', models.TextField(help_text='Ihr Feedback', max_length=2000, verbose_name='Nachricht')),
                ('sentiment', models.CharField(choices=[('positive', 'Positiv'), ('neutral', 'Neutral'), ('negativ', 'Negativ')], default='positive', max_length=8, verbose_name='Wie zufieden sind Sie mit der Suche?')),
                ('search_url', models.TextField(default=None)),
            ],
            options={
                'verbose_name': 'Feedback',
                'verbose_name_plural': 'Feedbacks',
            },
        ),
    ]
