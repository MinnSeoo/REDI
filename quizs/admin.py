from django.contrib import admin
from . import models


@admin.register(models.Answer)
class AnswerAdmin(admin.ModelAdmin):

    """Answer Admin Definition"""

    list_display = (
        "is_correct",
        "context",
    )
    list_filter = ("is_correct",)
    search_fields = ("quiz",)


@admin.register(models.Quiz)
class QuizAdmin(admin.ModelAdmin):

    """Quiz Admin Definition"""

    list_display = ("question", "points")
    search_fields = ("question",)
