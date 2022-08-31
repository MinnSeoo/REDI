from django.urls import path
from . import views


app_name = "quizs"

urlpatterns = [
    path("", views.QuizHomeView.as_view(), name="home"),
    path("find/", views.find_quiz, name="find"),
    path("add/", views.QuizAddView.as_view(), name="add"),
    path("list/", views.QuizListView.as_view(), name="list"),
    path("<int:pk>/solve/", views.QuizSolveView.as_view(), name="solve"),
    path("<int:pk>/detail/", views.QuizDetailView.as_view(), name="detail"),
    path("<int:pk>/edit/", views.QuizEditView.as_view(), name="edit"),
    path("<int:pk>/delete/", views.delete_quiz, name="delete"),
    path("<int:pk>/add-answer/", views.AnswerAddView.as_view(), name="add-answer"),
    path(
        "<int:quiz_pk>/<int:answer_pk>/edit/",
        views.AnswerEditView.as_view(),
        name="edit-answer",
    ),
    path(
        "<int:quiz_pk>/<int:answer_pk>/delete/",
        views.delete_answer,
        name="delete-answer",
    ),
    path("<int:quiz_pk>/<int:answer_pk>/check/", views.check_answer, name="check"),
    path("<int:pk>/correct/", views.CorrectAnswerView.as_view(), name="correct"),
    path("<int:pk>/wrong/", views.WrongAnswerView.as_view(), name="wrong"),
]
