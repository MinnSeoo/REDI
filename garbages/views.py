from django.views.generic import ListView, DetailView, FormView, UpdateView
from django.shortcuts import redirect, reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import reverse_lazy
from users import mixins
from . import models, forms


class GarbageListView(mixins.LoggedInOnlyView, ListView):

    model = models.Garbage
    paginate_by = 12
    # paginate_orphans =
    ordering = "-pk"
    context_object_name = "garbages"


class ReplacementListView(mixins.LoggedInOnlyView, ListView):

    model = models.Replacement
    paginate_by = 12
    # paginate_orphans =
    ordering = "-pk"
    context_object_name = "replacements"


class GarbageDetailView(mixins.LoggedInOnlyView, DetailView):

    model = models.Garbage


class ReplacementDetailView(mixins.LoggedInOnlyView, DetailView):

    model = models.Replacement


class GarbageAddView(mixins.SuperUserOnlyView, FormView):

    template_name = "garbages/garbage_add.html"
    form_class = forms.GarbageForm
    success_url = reverse_lazy("garbages:gb-list")

    def form_valid(self, form):

        # 작성한 모델을 저장

        garbage = form.save()
        garbage.save()
        form.save_m2m()
        messages.success(self.request, "쓰레기를 추가했습니다!")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["replacements"] = models.Replacement.objects.all()
        return context


class ReplacementAddView(mixins.SuperUserOnlyView, FormView):

    template_name = "garbages/replacement_add.html"
    form_class = forms.ReplacementForm
    success_url = reverse_lazy("garbages:rm-list")

    def form_valid(self, form):

        # 작성한 모델을 저장

        replacement = form.save()
        replacement.save()
        messages.success(self.request, "대체품을 추가했습니다!")
        return super().form_valid(form)


@login_required
@user_passes_test(lambda u: u.is_superuser)
def delete_garbage(request, pk):
    garbage = models.Garbage.objects.get(pk=pk)
    garbage.delete()
    messages.success(request, "쓰레기를 삭제했습니다!")
    return redirect(reverse("garbages:gb-list"))


@login_required
@user_passes_test(lambda u: u.is_superuser)
def delete_replacement(request, pk):
    replacement = models.Replacement.objects.get(pk=pk)
    replacement.delete()
    messages.success(request, "대체품을 삭제했습니다!")
    return redirect(reverse("garbages:rm-list"))


class GarbageEditView(mixins.SuperUserOnlyView, UpdateView):

    model = models.Garbage
    context_object_name = "garbage"
    form_class = forms.GarbageForm
    template_name = "garbages/garbage_update.html"
    success_url = reverse_lazy("garbages:gb-list")

    def form_valid(self, form):

        # 작성한 모델을 저장

        garbage = form.save()
        garbage.save()
        form.save_m2m()
        messages.success(self.request, "쓰레기를 수정했습니다!")
        return super().form_valid(form)

    def get_object(self):
        garbage = models.Garbage.objects.get(pk=self.kwargs["pk"])
        return garbage

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["replacements"] = models.Replacement.objects.all()
        return context


class ReplacementEditView(mixins.SuperUserOnlyView, UpdateView):

    model = models.Replacement
    context_object_name = "replacement"
    form_class = forms.ReplacementForm
    template_name = "garbages/replacement_update.html"
    success_url = reverse_lazy("garbages:rm-list")

    def form_valid(self, form):

        # 작성한 모델을 저장

        replacement = form.save()
        replacement.save()
        messages.success(self.request, "대체품을 수정했습니다!")
        return super().form_valid(form)

    def get_object(self):
        replacement = models.Replacement.objects.get(pk=self.kwargs["pk"])
        return replacement
