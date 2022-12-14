from django.db import models
from django.shortcuts import reverse
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.contrib.auth.validators import UnicodeUsernameValidator

from django.core.mail import EmailMessage
from django.template.loader import render_to_string
import uuid

from core.models import CustomModelImageField
from core.cal import Calendar
from datetime import datetime


class User(AbstractUser):

    """Custom User Model Definition"""

    EMAIL = "email"
    KAKAO = "kakao"
    DISCORD = "discord"

    LOGIN_METHOD_CHOICES = (
        (EMAIL, "Email"),
        (KAKAO, "Kakao"),
        (DISCORD, "Discord"),
    )

    username = models.CharField(
        "username",
        max_length=30,
        unique=True,
        help_text=("30글자 혹은 그 이하의 문자, 숫자, 그리고 ( @ . + - _ )만 가능합니다."),
        validators=[UnicodeUsernameValidator],
        error_messages={
            "unique": "닉네임이 이미 사용중입니다.",
        },
    )

    login_method = models.CharField(
        choices=LOGIN_METHOD_CHOICES, max_length=7, default=EMAIL
    )

    avatar = CustomModelImageField(upload_to="avatars", blank=True, null=True)

    exp = models.IntegerField(
        validators=[
            MinValueValidator(0),
        ],
        default=0,
    )

    bio = models.TextField(null=True, blank=True)
    email_verified = models.BooleanField(default=False)
    email_secret = models.CharField(max_length=120, default="")

    def get_absolute_url(self):
        return reverse("users:profile", kwargs={"username": self.username})

    def verify_email(self):
        if self.email_verified is False:
            secret = uuid.uuid4().hex[:20]
            self.email_secret = secret
            self.save()
            mail_subject = "REDI - 이메일 인증"
            message = render_to_string(
                "email/email_verification.html",
                {"name": self.username, "secret": secret},
            )
            to_email = self.email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.content_subtype = "html"
            send_email.send()

    def reset_password(self):
        password = uuid.uuid4().hex[:10].upper()
        self.set_password(password)
        self.save()
        mail_subject = "REDI - 비밀번호 초기화"
        message = render_to_string(
            "email/password_reset.html",
            {"name": self.username, "password": password},
        )
        to_email = self.email
        send_email = EmailMessage(mail_subject, message, to=[to_email])
        send_email.content_subtype = "html"
        send_email.send()

    def get_calender(self):
        now = datetime.now()
        calendar = Calendar(now.year, now.month)
        return calendar

    def get_histories(self):
        return self.histories.order_by("date")

    def get_amount_of_garbages(self):
        histories = self.get_histories()
        count = 0
        for history in histories:
            count += history.get_garbage_amount()
        return count

    def get_total_value(self):
        histories = self.get_histories()
        count = 0
        for history in histories:
            count += history.get_total_value()
        return count
