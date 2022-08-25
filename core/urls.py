from django.urls import path
from users import views

app_name = "core"

urlpatterns = [
    path("", views.UserHomeView.as_view(), name="home"),
]
