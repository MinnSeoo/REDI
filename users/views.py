from django.shortcuts import redirect, reverse
from django.urls import reverse_lazy
from django.views.generic import TemplateView, FormView
from django.contrib.auth import login, logout
from . import mixins, forms, models


class UserHomeView(mixins.LoggedInOnlyView, TemplateView):

    """
    This is a home view for those who are logged in.
    """

    template_name = "users/home.html"


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
        return super().form_valid(form)

    def get_success_url(self):
        # url에 next= 후에 뭔가 있다면 그곳으로, 아니면 home으로
        next_arg = self.request.GET.get("next")
        if next_arg is not None:
            return next_arg
        else:
            return reverse("core:home")


def log_out(request):
    logout(request)
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
        return super().form_valid(form)
