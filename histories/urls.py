from django.urls import path, include
from . import views


app_name = "histories"

historypatterns = [
    path("", views.HistoryLogsView.as_view(), name="log"),
    path("add/", views.LogAddView.as_view(), name="add"),
    path(
        "<int:log_pk>/delete",
        views.log_delete,
        name="log-delete",
    ),
    path(
        "<int:log_pk>/edit",
        views.LogEditView.as_view(),
        name="log-edit",
    ),
]

urlpatterns = [
    path("home/", views.HistorySummaryView.as_view(), name="home"),
    path("create/", views.create, name="create"),
    path("log/<int:pk>/<str:date>/", include(historypatterns)),
]
