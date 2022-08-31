from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.log_out, name="logout"),
    path("signup/", views.SignUpView.as_view(), name="signup"),
    path("<str:username>/", views.UserProfileView.as_view(), name="profile"),
    path("<str:username>/edit", views.UserProfileEditView.as_view(), name="edit"),
    path("<str:username>/update-password", views.UserPasswordChangeView.as_view(), name="password-update"),
]
