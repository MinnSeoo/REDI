from django import forms
from . import models


class PostForm(forms.ModelForm):
    class Meta:
        model = models.MyPost
        fields = ("title", "context", "picture")
        labels = {"title": "제목", "context": "내용", "picture": "사진 첨부"}

    def save(self, *args, **kwargs):
        return super().save(commit=False)


class CommentForm(forms.ModelForm):
    class Meta:
        model = models.Comment
        fields = ("context",)

    def save(self, *args, **kwargs):
        return super().save(commit=False)
