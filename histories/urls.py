from django.urls import path
from . import views


app_name = "histories"

urlpatterns = [
    path("home/", views.HistorySummaryView.as_view(), name="home"),
    path("create/", views.create, name="create"),
    path("log/<int:pk>/<str:date>/", views.HistoryLogsView.as_view(), name="log"),
    path("log/<int:pk>/<str:date>/add/", views.LogAddView.as_view(), name="add"),
    path(
        "log/<int:pk>/<str:date>/<int:log_pk>/delete",
        views.log_delete,
        name="log-delete",
    ),
    path(
        "log/<int:pk>/<str:date>/<int:log_pk>/edit",
        views.LogEditView.as_view(),
        name="log-edit",
    ),
]
