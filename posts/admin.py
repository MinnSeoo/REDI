from django.contrib import admin
from . import models


@admin.register(models.MyPost)
class PostAdmin(admin.ModelAdmin):

    """Post Admin Definition"""

    list_display = (
        "user",
        "likes",
        "title",
    )
    search_fields = ("user", "context")


@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):

    """Commnet Admin Definition"""

    list_display = (
        "user",
        "likes",
        "post",
    )
    search_fields = ("user", "context")
    list_filter = ("post",)
