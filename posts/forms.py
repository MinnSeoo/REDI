from django import forms
from . import models


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
