from django import forms
from . import models


class LogForm(forms.ModelForm):
    class Meta:
        model = models.Log
        amount = forms.IntegerField(min_value=1)
        fields = ("garbage", "amount")
        labels = {"garbage": "쓰레기", "amount": "수량"}

    def save(self):
        log = super().save(commit=False)
        return log


class MemoForm(forms.ModelForm):
    class Meta:
        model = models.History
        memo = forms.CharField(max_length=100)
        fields = ("memo",)
        label = {"memo": "한줄 메모"}
        widgets = {
            "memo": forms.TextInput(attrs={"placeholder": "메모를 적어주세요"}),
        }
