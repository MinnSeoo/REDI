# Generated by Django 4.1 on 2022-09-10 07:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("histories", "0006_alter_log_history"),
    ]

    operations = [
        migrations.AlterField(
            model_name="history",
            name="memo",
            field=models.TextField(max_length=300, null=True),
        ),
    ]
