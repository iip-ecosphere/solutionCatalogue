# Generated by Django 3.2.8 on 2021-10-13 14:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0014_merge_20211012_1940'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='inquiry',
            name='recipient',
        ),
        migrations.AlterField(
            model_name='componentlog',
            name='accessed',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Besucht'),
        ),
    ]
