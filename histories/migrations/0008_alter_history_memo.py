# Generated by Django 4.1 on 2022-09-10 07:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("histories", "0007_alter_history_memo"),
    ]

    operations = [
        migrations.AlterField(
            model_name="history",
            name="memo",
            field=models.TextField(blank=True, max_length=300, null=True),
        ),
    ]