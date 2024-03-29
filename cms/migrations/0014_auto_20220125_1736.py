# Generated by Django 3.2.11 on 2022-01-25 16:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0013_blog'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpage',
            name='slug',
            field=models.SlugField(default='', max_length=200, unique=True, verbose_name='URL'),
        ),
        migrations.AlterField(
            model_name='staticmenupage',
            name='slug',
            field=models.SlugField(default='', max_length=200, unique=True, verbose_name='URL'),
        ),
    ]
