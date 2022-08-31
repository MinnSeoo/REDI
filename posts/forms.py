from django import forms
from . import models


# 두 개를 하나로 합쳐도 될 듯


class PostAddForm(forms.ModelForm):
    class Meta:
        model = models.MyPost
        fields = ("title", "context", "picture")

    def save(self, *args, **kwargs):
        return super().save(commit=False)


class PostUpdateForm(forms.ModelForm):
    class Meta:
        model = models.MyPost
        fields = ("title", "context", "picture")

    def save(self, *args, **kwargs):
        return super().save(commit=False)
