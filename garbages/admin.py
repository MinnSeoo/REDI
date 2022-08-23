from django.contrib import admin
from . import models


@admin.register(models.Garbage)
class GarbageAdmin(admin.ModelAdmin):

    """Garbage Admin Definition"""

    list_display = ("name", "value")
    ordering = ("name",)
    list_filter = ("value",)
    filter_horizontal = ("replacements",)
    search_fields = ("name",)


@admin.register(models.Replacement)
class ReplacementAdmin(admin.ModelAdmin):

    """Replacement Admin Definition"""

    list_display = ("name",)
    ordering = ("name",)
    search_fields = ("name",)
