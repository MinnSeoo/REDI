import datetime
from django.db.models import Q
from django.views.generic import TemplateView, DetailView, FormView, UpdateView
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, reverse
from django.http import Http404
from users import mixins
from . import forms, models


class HistorySummaryView(mixins.LoggedInOnlyView, TemplateView):
    template_name = "histories/histories_home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user
        return context


def create(request):
    user = request.user
    date = request.GET.get("date")
    if date == "":
        return redirect(reverse("histories:home"))
    history = models.History.objects.create(user=user, date=date)
    return redirect(history.get_absolute_url())


class HistoryLogsView(mixins.LoggedInOnlyView, DetailView):

    model = models.History
    template_name = "histories/histories_logs.html"

    def get_object(self, queryset=None):
        history = get_history(self)
        if history.user.pk != self.request.user.pk:
            raise Http404()
        return history

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        date = self.kwargs.get("date")
        history = get_history(self)
        context["logs"] = history.logs.all()
        context["pk"] = self.kwargs.get("pk")
        context["date"] = date
        return context


def get_history(obj):
    date = obj.kwargs.get("date")
    year = int(date[:4])
    month = int(date[5:7])
    day = int(date[8:])
    history = models.History.objects.get(
        Q(user=obj.request.user), Q(date=datetime.datetime(year, month, day))
    )
    return history


class LogAddView(mixins.LoggedInOnlyView, FormView):

    form_class = forms.LogAddForm
    template_name = "histories/log_add.html"

    def get_success_url(self):
        return reverse(
            "histories:log",
            kwargs={"pk": self.kwargs.get("pk"), "date": self.kwargs.get("date")},
        )

    def form_valid(self, form):

        log = form.save()
        history = get_history(self)
        log.history = history
        log.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["pk"] = self.kwargs.get("pk")
        context["date"] = self.kwargs.get("date")
        return context


@login_required
def log_delete(request, pk, date, log_pk):
    models.Log.objects.get(pk=log_pk).delete()
    return redirect(reverse("histories:log", kwargs={"pk": pk, "date": date}))


class LogEditView(mixins.LoggedInOnlyView, UpdateView):

    model = models.Log
    context_object_name = "log"
    form_class = forms.LogForm
    template_name = "histories/log_edit.html"

    def get_success_url(self):
        return reverse(
            "histories:log",
            kwargs={"pk": self.kwargs.get("pk"), "date": self.kwargs.get("date")},
        )

    def get_object(self):
        log = models.Log.objects.get(pk=self.kwargs["log_pk"])
        return log
