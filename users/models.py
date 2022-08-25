from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator


class User(AbstractUser):

    """Custom User Model Definition"""

    EMAIL = "email"
    KAKAO = "kakao"
    GOOGLE = "google"
    DISCORD = "discord"

    LOGIN_METHOD_CHOICES = (
        (EMAIL, "Email"),
        (KAKAO, "Kakao"),
        (GOOGLE, "Google"),
        (DISCORD, "Discord"),
    )

    login_method = models.CharField(
        choices=LOGIN_METHOD_CHOICES, max_length=7, default=EMAIL
    )

    avatar = models.ImageField(upload_to="uploads/avatars", blank=True)

    exp = models.IntegerField(
        validators=[
            MinValueValidator(0),
        ],
        default=0,
    )
