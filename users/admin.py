from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models


@admin.register(models.User)
class CustomUserAdmin(UserAdmin):

    """Custom User Admin Definition"""

    fieldsets = UserAdmin.fieldsets + (
        ("Custom Profile", {"fields": ("avatar", "login_method")}),
    )

    list_filter = UserAdmin.list_filter + ("login_method",)

    list_display = ("username", "email", "is_superuser", "login_method")
