from django.db import models
from django.shortcuts import reverse
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

    avatar = models.ImageField(upload_to="avatars", blank=True, null=True)

    exp = models.IntegerField(
        validators=[
            MinValueValidator(0),
        ],
        default=0,
    )

    bio = models.TextField(null=True, blank=True)

    def get_absolute_url(self):
        return reverse("users:profile", kwargs={"username": self.username})
