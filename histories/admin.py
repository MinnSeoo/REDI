from django.contrib import admin
from . import models


@admin.register(models.Item)
class ItemAdmin(admin.ModelAdmin):

    """Admin Model Definition"""

    list_display = ("garbage", "amount", "history")

    search_fields = ("history", "garbage")


@admin.register(models.History)
class HistoryAdmin(admin.ModelAdmin):

    """History Admin Definition"""

    list_display = (
        "user",
        "date",
    )

    list_filter = ("date",)

    search_fields = ("user",)
