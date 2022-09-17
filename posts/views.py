from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, reverse
from django.views.generic import ListView, FormView, UpdateView
from django.contrib import messages
from users import mixins
from . import models, forms


class PostListView(mixins.LoggedInOnlyView, ListView):

    model = models.MyPost
    paginate_by = 3
    # paginate_orphans =
    ordering = "-pk"
    context_object_name = "posts"
    template_name = "posts/post_list.html"


class PostAddView(mixins.LoggedInOnlyView, FormView):

    form_class = forms.PostForm
    template_name = "posts/post_add.html"

    def form_valid(self, form):

        # 작성한 모델을 저장

        post = form.save()
        post.user = self.request.user
        post.save()
        messages.success(self.request, "글이 올려졌습니다!")
        return redirect(post.get_absolute_url())


class PostDetailView(mixins.LoginRequiredMixin, FormView):

    model = models.Comment
    form_class = forms.CommentForm
    template_name = "posts/post_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get("pk")
        context["post"] = models.MyPost.objects.get(pk=pk)
        return context

    def get_success_url(self):
        return reverse(
            "posts:detail",
            kwargs={"pk": self.kwargs.get("pk")},
        )

    def form_valid(self, form):

        comment = form.save()
        comment.user = self.request.user
        pk = self.kwargs.get("pk")
        post = models.MyPost.objects.get(pk=pk)
        comment.post = post
        comment.save()
        messages.success(self.request, "댓글을 달았습니다!")
        return super().form_valid(form)


@login_required
def comment_delete(request, post_pk, comment_pk):
    models.Comment.objects.get(pk=comment_pk).delete()
    messages.success(request, "댓글을 삭제했습니다!")
    return redirect(reverse("posts:detail", kwargs={"pk": post_pk}))


@login_required
def post_delete(request, pk):
    models.MyPost.objects.get(pk=pk).delete()
    messages.success(request, "글을 삭제했습니다!")
    return redirect(reverse("posts:home"))


class PostEditView(mixins.LoggedInOnlyView, UpdateView):

    model = models.MyPost
    context_object_name = "post"
    form_class = forms.PostForm
    template_name = "posts/post_update.html"

    def form_valid(self, form):

        # 작성한 모델을 저장

        post = form.save()
        post.save()
        messages.success(self.request, "글을 수정했습니다!")
        return redirect(post.get_absolute_url())

    def get_object(self):
        post = models.MyPost.objects.get(pk=self.kwargs["pk"])
        return post


def toggle_post_like(request, pk):
    post = models.MyPost.objects.get(pk=pk)

    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return redirect(reverse("posts:detail", kwargs={"pk": pk}))


def toggle_comment_like(request, pk):
    comment = models.Comment.objects.get(pk=pk)

    if request.user in comment.likes.all():
        comment.likes.remove(request.user)
    else:
        comment.likes.add(request.user)
    return redirect(reverse("posts:detail", kwargs={"pk": comment.post.pk}))
