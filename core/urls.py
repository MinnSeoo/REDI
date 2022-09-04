from django.urls import path
from users import views as user_views
from . import views

app_name = "core"

urlpatterns = [
    path("", user_views.UserHomeView.as_view(), name="home"),
    path("<str:name>/success/", views.SuccessView.as_view(), name="success"),
]
