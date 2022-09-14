import datetime
from django.db.models import Q
from django.views.generic import (
    TemplateView,
    DetailView,
    FormView,
    UpdateView,
    ListView,
)
from django.contrib import messages
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
        context["histories"] = self.request.user.get_histories()
        return context


class HistoryListView(mixins.LoggedInOnlyView, ListView):
    model = models.History
    paginate_by = 15
    # paginate_orphans =
    ordering = "date"
    context_object_name = "histories"
    template_name = "histories/histories_list.html"

    def get_queryset(self):
        return models.History.objects.filter(user=self.request.user)


@login_required
def create(request):
    user = request.user
    date = request.GET.get("date")
    if date == "":
        messages.warning(request, "날짜를 선택해주세요")
        return redirect(reverse("histories:home"))
    try:
        history = models.History.objects.get(user=user, date=date)
    except models.History.DoesNotExist:
        history = models.History.objects.create(user=user, date=date)
        messages.info(request, "기록이 생성되었습니다")
    return redirect(history.get_absolute_url())


@login_required
def history_delete(request, pk, date):
    models.History.objects.get(pk=pk).delete()
    messages.info(request, "기록이 제거되었습니다")
    return redirect(reverse("histories:list"))


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
        context["form"] = forms.MemoForm(instance=history)
        context["logs"] = history.logs.all()
        context["pk"] = self.kwargs.get("pk")
        context["date"] = date
        return context

    def post(self, request, pk, date):
        history = self.get_object()
        form = forms.MemoForm(request.POST)
        if form.is_valid():
            history.memo = form.cleaned_data.get("memo")
            history.save()
            return redirect(reverse("histories:log", kwargs={"pk": pk, "date": date}))


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

    form_class = forms.LogForm
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
        messages.success(self.request, "세부기록을 추가했습니다.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["pk"] = self.kwargs.get("pk")
        context["date"] = self.kwargs.get("date")
        return context


@login_required
def log_delete(request, pk, date, log_pk):
    models.Log.objects.get(pk=log_pk).delete()
    messages.success(request, "세부기록을 제거했습니다.")
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

    def form_valid(self, form):
        log = form.save()
        log.save()
        messages.success(self.request, "세부기록을 수정했습니다.")
        return super().form_valid(form)

    def get_object(self):
        log = models.Log.objects.get(pk=self.kwargs["log_pk"])
        return log
