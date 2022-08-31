from django import forms
from . import models


class QuizForm(forms.ModelForm):
    class Meta:
        model = models.Quiz
        points = forms.IntegerField(min_value=1)
        fields = ("question", "points")

    def save(self, *args, **kwargs):
        return super().save(commit=False)


class AnswerForm(forms.ModelForm):
    class Meta:
        model = models.Answer
        fields = ("context", "is_correct")

    def save(self, *args, **kwargs):
        return super().save(commit=False)
