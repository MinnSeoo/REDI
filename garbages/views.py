from django.views.generic import ListView, DetailView, FormView, UpdateView
from django.shortcuts import redirect, reverse
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from users import mixins
from . import models, forms


class GarbageListView(mixins.LoggedInOnlyView, ListView):

    model = models.Garbage
    paginate_by = 3
    # paginate_orphans =
    ordering = "-pk"
    context_object_name = "garbages"


class ReplacementListView(mixins.LoggedInOnlyView, ListView):

    model = models.Replacement
    paginate_by = 3
    # paginate_orphans =
    ordering = "-pk"
    context_object_name = "replacements"


class GarbageDetailView(mixins.LoggedInOnlyView, DetailView):

    model = models.Garbage


class ReplacementDetailView(mixins.LoggedInOnlyView, DetailView):

    model = models.Replacement


class GarbageAddView(mixins.LoggedInOnlyView, mixins.SuperUserOnlyView, FormView):

    template_name = "garbages/garbage_add.html"
    form_class = forms.GarbageForm
    success_url = reverse_lazy("garbages:gb-list")

    def form_valid(self, form):

        # 작성한 모델을 저장

        garbage = form.save()
        garbage.save()
        form.save_m2m()
        return super().form_valid(form)


class ReplacementAddView(mixins.LoggedInOnlyView, mixins.SuperUserOnlyView, FormView):

    template_name = "garbages/replacement_add.html"
    form_class = forms.ReplacementForm
    success_url = reverse_lazy("garbages:rm-list")

    def form_valid(self, form):

        # 작성한 모델을 저장

        replacement = form.save()
        replacement.save()
        return super().form_valid(form)


# superuser_required decorator로 superuser만 이 화면을 볼 수 있도록 해야 함
@login_required
def delete_garbage(request, pk):
    garbage = models.Garbage.objects.get(pk=pk)
    garbage.delete()
    return redirect(reverse("garbages:gb-list"))


@login_required
def delete_replacement(request, pk):
    replacement = models.Replacement.objects.get(pk=pk)
    replacement.delete()
    return redirect(reverse("garbages:rm-list"))


class GarbageEditView(mixins.LoggedInOnlyView, mixins.SuperUserOnlyView, UpdateView):

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
        return super().form_valid(form)

    def get_object(self):
        garbage = models.Garbage.objects.get(pk=self.kwargs["pk"])
        return garbage


class ReplacementEditView(
    mixins.LoggedInOnlyView, mixins.SuperUserOnlyView, UpdateView
):

    model = models.Replacement
    context_object_name = "replacement"
    form_class = forms.ReplacementForm
    template_name = "garbages/replacement_update.html"
    success_url = reverse_lazy("garbages:rm-list")

    def form_valid(self, form):

        # 작성한 모델을 저장

        replacement = form.save()
        replacement.save()
        return super().form_valid(form)

    def get_object(self):
        replacement = models.Replacement.objects.get(pk=self.kwargs["pk"])
        return replacement
