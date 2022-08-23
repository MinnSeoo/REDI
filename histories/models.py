from django.db import models
from django.core.validators import MinValueValidator


class History(models.Model):

    user = models.ForeignKey(
        "users.User", related_name="histories", on_delete=models.CASCADE
    )
    garbage = models.ForeignKey(
        "garbages.Garbage", related_name="histories", on_delete=models.SET_NULL, null=tr
    )
    amount = models.IntegerField(validators=[])
