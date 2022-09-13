from django import forms
from . import models


class GarbageForm(forms.ModelForm):
    class Meta:
        model = models.Garbage
        value = forms.IntegerField(min_value=1)
        fields = ("icon", "name", "description", "value", "replacements")
        labels = {
            "icon": "아이콘",
            "name": "이름",
            "description": "설명",
            "value": "환경에 영향을 끼치는 정도",
            "replacements": "대체품",
        }

    def save(self, *args, **kwargs):
        return super().save(commit=False)


class ReplacementForm(forms.ModelForm):
    class Meta:
        model = models.Replacement
        fields = ("icon", "name", "description")
        labels = {"icon": "아이콘", "name": "이름", "description": "설명"}

    def save(self, *args, **kwargs):
        return super().save(commit=False)
