from django.urls import path, include
from . import views

app_name = "users"

loginpatterns = [
    path("", views.LoginView.as_view(), name="login"),
    path("kakao/", views.kakao_login, name="kakao-login"),
    path("kakao/callback/", views.kakao_callback, name="kakao-callback"),
    path("discord/", views.discord_login, name="discord-login"),
    path("discord/callback/", views.discord_callback, name="discord-callback"),
]

profilepatterns = [
    path("", views.UserProfileView.as_view(), name="profile"),
    path("edit", views.UserProfileEditView.as_view(), name="edit"),
    path(
        "update-password",
        views.UserPasswordChangeView.as_view(),
        name="password-update",
    ),
]

urlpatterns = [
    path("login/", include(loginpatterns)),
    path("logout/", views.log_out, name="logout"),
    path("signup/", views.SignUpView.as_view(), name="signup"),
    path("reset-password/", views.PasswordResetView.as_view(), name="reset-password"),
    path(
        "verify/<str:secret>", views.complete_verification, name="complete-verification"
    ),
    path("<str:username>/", include(profilepatterns)),
]
