# Generated by Django 4.1 on 2022-09-10 02:08

import django.contrib.auth.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0010_alter_user_avatar"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="username",
            field=models.CharField(
                error_messages={"unique": "닉네임이 이미 사용중입니다."},
                help_text="30글자 혹은 그 이하의 문자, 숫자, 그리고 ( @ . + - _ )만 가능합니다.",
                max_length=30,
                unique=True,
                validators=[django.contrib.auth.validators.UnicodeUsernameValidator],
                verbose_name="username",
            ),
        ),
    ]
