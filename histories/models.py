from django.db import models
from django.core.validators import MinValueValidator


class Item(models.Model):

    """History Model Definition"""

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
        "History", related_name="items", on_delete=models.CASCADE
    )


class History(models.Model):

    """History Model Definition"""

    user = models.ForeignKey(
        "users.User", related_name="histories", on_delete=models.CASCADE
    )
    date = models.DateField()
    memo = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.user.username + " - " + str(self.date)
