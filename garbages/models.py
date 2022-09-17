from django.db import models
from django.core.validators import MinValueValidator
from core.models import CustomModelImageField


class BaseItem(models.Model):

    """Base Item Definition"""

    name = models.CharField(max_length=30, unique=True)
    icon = CustomModelImageField(upload_to="icons")
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Replacement(BaseItem):

    """Replacement Model Definition"""


class Garbage(BaseItem):

    """Garbage Model Definition"""

    value = models.IntegerField(
        validators=[
            MinValueValidator(1),
        ]
    )
    replacements = models.ManyToManyField(
        "Replacement", related_name="garbages", blank=True
    )
