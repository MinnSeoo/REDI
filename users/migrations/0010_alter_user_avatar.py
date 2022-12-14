# Generated by Django 4.1 on 2022-09-07 04:22

import core.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0009_alter_user_login_method"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="avatar",
            field=core.models.CustomModelImageField(
                blank=True, null=True, upload_to="avatars"
            ),
        ),
    ]
