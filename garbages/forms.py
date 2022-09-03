from django import forms
from . import models


class GarbageForm(forms.ModelForm):
    class Meta:
        model = models.Garbage
        value = forms.IntegerField(min_value=1)
        fields = ("icon", "name", "description", "value", "replacements")

    def save(self, *args, **kwargs):
        return super().save(commit=False)


class ReplacementForm(forms.ModelForm):
    class Meta:
        model = models.Replacement
        fields = ("icon", "name", "description")

    def save(self, *args, **kwargs):
        return super().save(commit=False)
