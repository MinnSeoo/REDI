from random import shuffle
from django.db import models
from django.shortcuts import reverse
from django.core.validators import MinValueValidator, MaxValueValidator


class Answer(models.Model):
    quiz = models.ForeignKey("Quiz", related_name="answers", on_delete=models.CASCADE)
    context = models.CharField(max_length=30)
    is_correct = models.BooleanField(default=False)


class Quiz(models.Model):

    question = models.CharField(max_length=200)
    points = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(100)]
    )

    def __str__(self):
        return self.question

    def get_every_answers(self):
        my_list = list(self.answers.all())
        shuffle(my_list)
        return my_list

    def get_absolute_url(self):
        return reverse("quizs:detail", kwargs={"pk": self.pk})
