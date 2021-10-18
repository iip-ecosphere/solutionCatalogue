# Generated by Django 3.2.8 on 2021-10-17 17:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("cms", "0002_auto_20211017_1735"),
    ]

    operations = [
        migrations.AddField(
            model_name="staticmenupage",
            name="parent",
            field=models.ForeignKey(
                blank=True,
                default=None,
                on_delete=django.db.models.deletion.PROTECT,
                to="cms.staticmenupage",
                verbose_name="Oberpunkt",
            ),
        ),
    ]
