from django import forms
from . import models


class LogForm(forms.ModelForm):
    class Meta:
        model = models.Log
        amount = forms.IntegerField(min_value=1)
        fields = ("garbage", "amount")

    def save(self):
        log = super().save(commit=False)
        return log
