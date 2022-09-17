from django.urls import path, include
from . import views


app_name = "quizs"


quizpatterns = [
    path("solve/", views.QuizSolveView.as_view(), name="solve"),
    path("detail/", views.QuizDetailView.as_view(), name="detail"),
    path("edit/", views.QuizEditView.as_view(), name="edit"),
    path("delete/", views.delete_quiz, name="delete"),
    path("add-answer/", views.AnswerAddView.as_view(), name="add-answer"),
    path("correct/", views.CorrectAnswerView.as_view(), name="correct"),
    path("wrong/", views.WrongAnswerView.as_view(), name="wrong"),
]

answerpatterns = [
    path("<int:answer_pk>/edit/", views.AnswerEditView.as_view(), name="edit-answer"),
    path("<int:answer_pk>/delete/", views.delete_answer, name="delete-answer"),
    path("<int:answer_pk>/check/", views.check_answer, name="check"),
]


urlpatterns = [
    path("", views.QuizHomeView.as_view(), name="home"),
    path("find/", views.find_quiz, name="find"),
    path("add/", views.QuizAddView.as_view(), name="add"),
    path("list/", views.QuizListView.as_view(), name="list"),
    path("<int:pk>/", include(quizpatterns)),
    path("<int:quiz_pk>/", include(answerpatterns)),
]
