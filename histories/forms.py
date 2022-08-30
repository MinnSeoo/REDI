from django import forms
from . import models


class LogAddForm(forms.ModelForm):
    class Meta:
        model = models.Log
        amount = forms.IntegerField(min_value=1)
        fields = ("garbage", "amount")

    def save(self):
        log = super().save(commit=False)
        return log


class LogEditForm(forms.ModelForm):
    class Meta:
        model = models.Log
        amount = forms.IntegerField(min_value=1)
        fields = ("garbage", "amount")
