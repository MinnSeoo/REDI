from django.shortcuts import redirect, reverse
from django.views.generic import TemplateView, FormView, CreateView
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
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = models.User.objects.get(email=email)
        if user.check_password(password):
            login(self.request, user)
        return super().form_valid(form)

    def get_success_url(self):
        next_arg = self.request.GET.get("next")
        if next_arg is not None:
            return next_arg
        else:
            return reverse("core:home")


def log_out(request):
    logout(request)
    return redirect(reverse("users:login"))


class SignUpView(mixins.LoggedOutOnlyView, CreateView):
    
    

    pass
