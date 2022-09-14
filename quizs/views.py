from random import choice
from django.shortcuts import redirect, reverse
from django.contrib.auth.decorators import login_required
from django.views.generic import (
    TemplateView,
    DetailView,
    FormView,
    UpdateView,
    ListView,
)
from django.contrib import messages
from users import mixins
from . import models, forms


class QuizHomeView(mixins.LoggedInOnlyView, TemplateView):
    template_name = "quizs/quiz_home.html"


def find_quiz(request):
    quiz = choice(list(models.Quiz.objects.all()))
    return redirect(reverse("quizs:solve", kwargs={"pk": quiz.pk}))


class QuizSolveView(mixins.LoggedInOnlyView, DetailView):

    model = models.Quiz
    template_name = "quizs/quiz_solve.html"
    context_object_name = "quiz"

    def get_object(self):
        pk = self.kwargs.get("pk")
        quiz = models.Quiz.objects.get(pk=pk)
        return quiz


def check_answer(request, quiz_pk, answer_pk):
    quiz = models.Quiz.objects.get(pk=quiz_pk)
    answer = models.Answer.objects.get(pk=answer_pk)
    if answer.is_correct:
        request.user.exp += quiz.points
        request.user.save()
        return redirect(reverse("quizs:correct", kwargs={"pk": quiz_pk}))
    else:
        return redirect(reverse("quizs:wrong", kwargs={"pk": quiz_pk}))


class AnswerCheckBaseView(mixins.LoggedInOnlyView, TemplateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get("pk")
        quiz = models.Quiz.objects.get(pk=pk)
        context["quiz"] = quiz
        return context


class CorrectAnswerView(AnswerCheckBaseView):

    template_name = "quizs/answer_correct.html"


class WrongAnswerView(AnswerCheckBaseView):

    template_name = "quizs/answer_wrong.html"


class QuizAddView(mixins.LoggedInOnlyView, mixins.SuperUserOnlyView, FormView):

    template_name = "quizs/quiz_add.html"
    form_class = forms.QuizForm

    def form_valid(self, form):
        quiz = form.save()
        quiz.save()
        messages.success(self.request, "퀴즈를 추가했습니다!")
        return redirect(reverse("quizs:detail", kwargs={"pk": quiz.pk}))


class QuizEditView(mixins.LoggedInOnlyView, mixins.SuperUserOnlyView, UpdateView):

    model = models.Quiz
    context_object_name = "quiz"
    form_class = forms.QuizForm
    template_name = "quizs/quiz_edit.html"

    def form_valid(self, form):
        quiz = form.save()
        quiz.save()
        pk = self.kwargs.get("pk")
        messages.success(self.request, "퀴즈를 수정했습니다!")
        return redirect(reverse("quizs:detail", kwargs={"pk": pk}))

    def get_object(self):
        quiz = models.Quiz.objects.get(pk=self.kwargs["pk"])
        return quiz


@login_required
def delete_quiz(request, pk):
    quiz = models.Quiz.objects.get(pk=pk)
    quiz.delete()
    messages.success(request, "퀴즈를 제거했습니다!")
    return redirect(reverse("quizs:list"))


class QuizListView(mixins.LoggedInOnlyView, mixins.SuperUserOnlyView, ListView):
    model = models.Quiz
    paginate_by = 3
    # paginate_orphans =
    ordering = "-pk"
    context_object_name = "quizs"


class QuizDetailView(mixins.LoggedInOnlyView, mixins.SuperUserOnlyView, DetailView):

    model = models.Quiz
    template_name = "quizs/quiz_detail.html"
    context_object_name = "quiz"

    def get_object(self):
        pk = self.kwargs.get("pk")
        quiz = models.Quiz.objects.get(pk=pk)
        return quiz


class AnswerAddView(mixins.LoggedInOnlyView, mixins.SuperUserOnlyView, FormView):

    template_name = "quizs/answer_add.html"
    form_class = forms.AnswerForm

    def form_valid(self, form):
        answer = form.save()
        pk = self.kwargs.get("pk")
        answer.quiz = models.Quiz.objects.get(pk=pk)
        answer.save()
        messages.success(self.request, "답변을 추가했습니다!")
        return redirect(reverse("quizs:detail", kwargs={"pk": pk}))


class AnswerEditView(mixins.LoggedInOnlyView, mixins.SuperUserOnlyView, UpdateView):

    model = models.Answer
    context_object_name = "answer"
    form_class = forms.AnswerForm
    template_name = "quizs/answer_edit.html"

    def form_valid(self, form):
        answer = form.save()
        answer.save()
        pk = self.kwargs.get("quiz_pk")
        messages.success(self.request, "답변을 수정했습니다!")
        return redirect(reverse("quizs:detail", kwargs={"pk": pk}))

    def get_object(self):
        answer = models.Answer.objects.get(pk=self.kwargs["answer_pk"])
        return answer


@login_required
def delete_answer(request, quiz_pk, answer_pk):
    answer = models.Answer.objects.get(pk=answer_pk)
    answer.delete()
    messages.success(request, "답변을 제거했습니다!")
    return redirect(reverse("quizs:detail", kwargs={"pk": quiz_pk}))
