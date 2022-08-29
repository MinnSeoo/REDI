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
    ordering = "pk"
    context_object_name = "garbages"


class GarbageDetailView(mixins.LoggedInOnlyView, DetailView):

    model = models.Garbage


class GarbageAddView(mixins.LoggedInOnlyView, mixins.SuperUserOnlyView, FormView):

    template_name = "garbages/garbage_add.html"
    form_class = forms.GarbageAddForm
    success_url = reverse_lazy("garbages:list")

    def form_valid(self, form):

        # 작성한 모델을 저장

        garbage = form.save()
        garbage.save()
        form.save_m2m()
        return super().form_valid(form)


# superuser_required decorator로 superuser만 이 화면을 볼 수 있도록 해야 함
@login_required
def delete_garbage(request, pk):
    garbage = models.Garbage.objects.get(pk=pk)
    garbage.delete()
    return redirect(reverse("garbages:list"))


class GarbageEditView(mixins.LoggedInOnlyView, mixins.SuperUserOnlyView, UpdateView):

    model = models.Garbage
    context_object_name = "garbage"
    form_class = forms.GarbageUpdateForm
    template_name = "garbages/garbage_update.html"
    success_url = reverse_lazy("garbages:list")

    def form_valid(self, form):

        # 작성한 모델을 저장

        garbage = form.save()
        garbage.save()
        form.save_m2m()
        return super().form_valid(form)

    def get_object(self):
        garbage = models.Garbage.objects.get(pk=self.kwargs["pk"])
        return garbage
