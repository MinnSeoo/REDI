from django.db import models
from django.shortcuts import reverse
from django.core.validators import MinValueValidator


class Log(models.Model):

    """Log Model Definition"""

    garbage = models.ForeignKey(
        "garbages.Garbage",
        related_name="histories",
        on_delete=models.CASCADE,
    )
    amount = models.IntegerField(
        validators=[
            MinValueValidator(1),
        ]
    )
    history = models.ForeignKey(
        "History", related_name="logs", on_delete=models.CASCADE
    )

    def get_absolute_url(self):
        return reverse(
            "histories:log-edit",
            kwargs={
                "pk": self.history.user.pk,
                "date": str(self.history.date),
                "log_pk": self.pk,
            },
        )


import random


class History(models.Model):

    """History Model Definition"""

    user = models.ForeignKey(
        "users.User", related_name="histories", on_delete=models.CASCADE
    )
    date = models.DateField()
    memo = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.user.username + " - " + str(self.date)

    def get_absolute_url(self):
        return reverse(
            "histories:log", kwargs={"pk": self.user.pk, "date": str(self.date)}
        )

    def random_value(self):
        return random.randint(1, 50)
