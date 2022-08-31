from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, reverse
from django.views.generic import ListView, FormView, DetailView, UpdateView
from users import mixins
from . import models, forms


class PostListView(mixins.LoggedInOnlyView, ListView):

    model = models.MyPost
    paginate_by = 3
    # paginate_orphans =
    ordering = "-pk"
    context_object_name = "posts"
    template_name = "posts/list.html"


class PostAddView(mixins.LoggedInOnlyView, FormView):

    form_class = forms.PostAddForm
    template_name = "posts/post_add.html"

    def form_valid(self, form):

        # 작성한 모델을 저장

        post = form.save()
        post.user = self.request.user
        post.save()
        return redirect(post.get_absolute_url())


class PostDetailView(mixins.LoginRequiredMixin, DetailView):

    model = models.MyPost
    template_name = "posts/post_detail.html"
    context_object_name = "post"


@login_required
def post_delete(request, pk):
    models.MyPost.objects.get(pk=pk).delete()
    return redirect(reverse("posts:home"))


class PostEditView(mixins.LoggedInOnlyView, UpdateView):

    model = models.MyPost
    context_object_name = "post"
    form_class = forms.PostUpdateForm
    template_name = "posts/post_update.html"

    def form_valid(self, form):

        # 작성한 모델을 저장

        post = form.save()
        post.save()
        return redirect(post.get_absolute_url())

    def get_object(self):
        post = models.MyPost.objects.get(pk=self.kwargs["pk"])
        return post
