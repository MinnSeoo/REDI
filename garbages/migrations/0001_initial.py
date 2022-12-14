# Generated by Django 4.1 on 2022-08-22 11:43

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="BaseItem",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=30, unique=True)),
                ("icon", models.ImageField(upload_to="icons")),
                ("discription", models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name="Replacement",
            fields=[
                (
                    "baseitem_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="garbages.baseitem",
                    ),
                ),
            ],
            bases=("garbages.baseitem",),
        ),
        migrations.CreateModel(
            name="Garbage",
            fields=[
                (
                    "baseitem_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="garbages.baseitem",
                    ),
                ),
                (
                    "value",
                    models.IntegerField(
                        validators=[django.core.validators.MinValueValidator(1)]
                    ),
                ),
                (
                    "replacements",
                    models.ManyToManyField(
                        related_name="garbages", to="garbages.replacement"
                    ),
                ),
            ],
            bases=("garbages.baseitem",),
        ),
    ]
