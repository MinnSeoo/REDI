import os
import requests
from requests.exceptions import SSLError
from django.shortcuts import redirect, reverse
from django.urls import reverse_lazy
from django.views.generic import TemplateView, FormView, DetailView, UpdateView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from . import mixins, forms, models


class UserHomeView(mixins.LoggedInOnlyView, TemplateView):

    """
    This is a home view for those who are logged in.
    """

    template_name = "users/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        qs = models.User.objects.order_by("-exp")
        count = qs.count()
        if count > 10:
            rank_list = list(qs)[:10]
        else:
            rank_list = list(qs)

        rank_list = list(map(lambda user: {rank_list.index(user) + 1: user}, rank_list))

        context["user_rank_list"] = rank_list
        return context


class LoginView(mixins.LoggedOutOnlyView, FormView):

    template_name = "users/login.html"

    form_class = forms.LoginForm

    def form_valid(self, form):

        # form에서 email과 password를 가져옴
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")

        # User object 중에서 email이 가져온 email과 같은 object를 가져옴
        user = models.User.objects.get(email=email)

        # 가져온 user의 password가 correct하다면 로그인
        if user.check_password(password):
            login(self.request, user)
        # success url로 redirect
        messages.success(self.request, f"안녕하세요, {user.username}님!")
        return super().form_valid(form)

    def get_success_url(self):
        # url에 next= 후에 뭔가 있다면 그곳으로, 아니면 home으로
        next_arg = self.request.GET.get("next")
        if next_arg is not None:
            return next_arg
        else:
            return reverse("core:home")


@login_required
def log_out(request):
    logout(request)
    messages.info(request, "다음에 봐요 :)")
    return redirect(reverse("users:login"))


class SignUpView(mixins.LoggedOutOnlyView, FormView):

    template_name = "users/signup.html"
    form_class = forms.SignUpForm
    success_url = reverse_lazy("core:home")

    def form_valid(self, form):

        # SignUpForm에서 작성한 모델을 저장
        form.save()

        # 이하 login과 같음
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = models.User.objects.get(email=email)
        if user.check_password(password):
            login(self.request, user)
        user.verify_email()
        messages.success(self.request, "환영합니다! 인증을 위한 이메일을 보냈으니 스팸함을 확인해주세요!")
        return super().form_valid(form)


class UserProfileView(mixins.LoggedInOnlyView, DetailView):

    model = models.User
    template_name = "users/profile.html"

    def get_object(self, queryset=None):
        username = self.kwargs.get("username")
        try:
            user = models.User.objects.get(username=username)
            return user
        except models.User.DoesNotExist:
            messages.error(self.request, "유저가 존재하지 않습니다.")
            return redirect(reverse("core:home"))


class UserProfileEditView(mixins.LoggedInOnlyView, UpdateView):
    model = models.User
    context_object_name = "user"
    form_class = forms.UserEditForm
    template_name = "users/edit.html"

    def get_success_url(self, username):
        return redirect(reverse("users:profile", kwargs={"username": username}))

    def form_valid(self, form):
        username = form.save()
        messages.success(self.request, "프로필 정보를 변경했습니다!")
        return self.get_success_url(username=username)

    def get_object(self):
        user = models.User.objects.get(username=self.kwargs["username"])
        return user


class UserPasswordChangeView(
    mixins.LoggedInOnlyView, SuccessMessageMixin, PasswordChangeView
):

    template_name = "users/update_password.html"
    success_message = "비밀번호가 변경되었습니다!"

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        form.fields["old_password"].label = "기존 비밀번호"
        form.fields["new_password1"].label = "새 비밀번호"
        form.fields["new_password2"].label = "비밀번호 확인"
        return form

    def get_success_url(self):
        return self.request.user.get_absolute_url()


def complete_verification(request, secret):
    try:
        user = models.User.objects.get(email_secret=secret)
        user.email_verified = True
        user.email_secret = ""
        user.save()
        messages.success(request, "성공적으로 인증되었습니다!")
    except models.User.DoesNotExist:
        messages.error(request, "유저가 존재하지 않습니다")
    return redirect(reverse("core:home"))


class PasswordResetView(mixins.LoggedOutOnlyView, FormView):

    form_class = forms.ResetPasswordForm
    template_name = "users/reset_password.html"

    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        user = models.User.objects.get(email=email)
        user.reset_password()
        messages.info(self.request, "초기화된 비밀번호를 이메일로 보냈습니다. 스팸함을 확인해주세요!")
        return redirect(reverse("users:login"))


def kakao_login(request):
    client_id = os.environ.get("KAKAO_ID")
    redirect_uri = "http://localhost:8000/users/login/kakao/callback"
    return redirect(
        f"https://kauth.kakao.com/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code"
    )


class KakaoException(Exception):
    pass


def kakao_callback(request):
    try:
        code = request.GET.get("code")
        client_id = os.environ.get("KAKAO_ID")
        redirect_uri = "http://localhost:8000/users/login/kakao/callback"
        token_request = requests.get(
            f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={client_id}&redirect_uri={redirect_uri}&code={code}"
        )
        token_json = token_request.json()
        error = token_json.get("error", None)
        if error is not None:
            raise KakaoException("토큰을 받는 데 문제가 생겼습니다")
        access_token = token_json.get("access_token")
        profile_request = requests.get(
            "https://kapi.kakao.com/v2/user/me",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        profile_json = profile_request.json()
        kakao_account = profile_json.get("kakao_account")
        email = kakao_account.get("email", None)
        if email is None:
            raise KakaoException("이메일을 받지 못했습니다")
        properties = profile_json.get("properties")
        username = properties.get("nickname")
        try:
            user = models.User.objects.get(email=email)
            if user.login_method != models.User.KAKAO:
                raise KakaoException("계정의 로그인 방법이 카카오톡이 아닙니다")
        except models.User.DoesNotExist:
            user = models.User.objects.create(
                email=email,
                username=username,
                login_method=models.User.KAKAO,
                email_verified=True,
            )
            user.set_unusable_password()
            user.save()
        login(request, user)
        messages.success(request, f"안녕하세요, {user.username}님!")
        return redirect(reverse("core:home"))
    except KakaoException as e:
        messages.error(request, e)
        return redirect(reverse("users:login"))


def discord_login(request):
    client_id = os.environ.get("DISCORD_ID")
    redirect_uri = "http://localhost:8000/users/login/discord/callback"
    return redirect(
        f"https://discord.com/oauth2/authorize?response_type=code&client_id={client_id}&redirect_uri={redirect_uri}&prompt=consent&scope=identify%20email"
    )


class DiscordException(Exception):
    pass


def discord_callback(request):
    try:
        code = request.GET.get("code")
        token_json = exchange_code(code)
        if token_json is not None:
            access_token = token_json["access_token"]
            response = requests.get(
                "https://discord.com/api/v10/users/@me",
                headers={"Authorization": f"Bearer {access_token}"},
            )
            user_json = response.json()
            username = user_json["username"]
            email = user_json["email"]
            try:
                user = models.User.objects.get(email=email)
                if user.login_method != models.User.DISCORD:
                    raise DiscordException("계정의 로그인 방법이 디스코드가 아닙니다")
            except models.User.DoesNotExist:
                user = models.User.objects.create(
                    email=email,
                    username=username,
                    login_method=models.User.DISCORD,
                    email_verified=True,
                )
                user.set_unusable_password()
                user.save()
            login(request, user)
            messages.success(request, f"안녕하세요, {user.username}님!")
            return redirect(reverse("core:home"))
        else:
            raise DiscordException("토큰을 받는 데 문제가 생겼습니다")
    except DiscordException as e:
        messages.error(request, e)
        return redirect(reverse("users:login"))


def exchange_code(code):
    try:
        redirect_uri = "http://localhost:8000/users/login/discord/callback"
        client_id = os.environ.get("DISCORD_ID")
        client_secret = os.environ.get("DISCORD_SECRET")
        data = {
            "client_id": client_id,
            "client_secret": client_secret,
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": redirect_uri,
        }
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        r = requests.post(
            "https://discord.com/api/oauth2/token", data=data, headers=headers
        )
        r.raise_for_status()
        return r.json()
    except SSLError:
        return None
