from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.http import Http404
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin


class LoggedOutOnlyView(UserPassesTestMixin):

    """user가 login이 되어있으면 home으로 이동"""

    def test_func(self):
        return not self.request.user.is_authenticated

    def handle_no_permission(self):
        return redirect("core:home")


class LoggedInOnlyView(LoginRequiredMixin):

    """user가 login이 되어있지 않으면 login으로 이동"""

    login_url = reverse_lazy("users:login")


class SuperUserOnlyView(UserPassesTestMixin):

    """user가 superuser가 아니면 404 에러"""

    def test_func(self):
        return self.request.user.is_superuser

    def handle_no_permission(self):
        raise Http404()
