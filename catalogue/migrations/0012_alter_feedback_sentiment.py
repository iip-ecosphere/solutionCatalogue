# Generated by Django 3.2.7 on 2021-10-05 21:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0011_auto_20211005_1359'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedback',
            name='sentiment',
            field=models.CharField(choices=[('positive', 'Positiv'), ('neutral', 'Neutral'), ('negativ', 'Negativ')], default='positive', max_length=8, verbose_name='Wie zufrieden sind Sie mit der Suche?'),
        ),
    ]
