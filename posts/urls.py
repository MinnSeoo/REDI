from django.urls import path
from . import views

app_name = "posts"

urlpatterns = [
    path("", views.PostListView.as_view(), name="home"),
    path("add/", views.PostAddView.as_view(), name="add"),
    path("<int:pk>/", views.PostDetailView.as_view(), name="detail"),
    path("<int:pk>/delete/", views.post_delete, name="post-delete"),
    path(
        "<int:post_pk>/<int:comment_pk>/delete/",
        views.comment_delete,
        name="comment-delete",
    ),
    path("<int:pk>/edit/", views.PostEditView.as_view(), name="edit"),
    path("<int:pk>/toggle_post_like/", views.toggle_post_like, name="toggle-post-like"),
    path(
        "<int:pk>/toggle_comment_like/",
        views.toggle_comment_like,
        name="toggle-comment-like",
    ),
]
