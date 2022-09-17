from django.db import models
from django.forms import ImageField
from django.forms.widgets import FileInput


class CustomFileInput(FileInput):
    template_name = "partials/input/file.html"


class CustomFormImageField(ImageField):
    widget = CustomFileInput


class CustomModelImageField(models.ImageField):
    def formfield(self, **kwargs):
        return super().formfield(
            **{
                "form_class": CustomFormImageField,
                **kwargs,
            }
        )
