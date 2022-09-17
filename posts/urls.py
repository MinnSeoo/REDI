from django.urls import path, include
from . import views

app_name = "posts"

postpatterns = [
    path("", views.PostDetailView.as_view(), name="detail"),
    path("delete/", views.post_delete, name="post-delete"),
    path("edit/", views.PostEditView.as_view(), name="edit"),
    path("toggle_post_like/", views.toggle_post_like, name="toggle-post-like"),
    path(
        "toggle_comment_like/",
        views.toggle_comment_like,
        name="toggle-comment-like",
    ),
]

urlpatterns = [
    path("", views.PostListView.as_view(), name="home"),
    path("add/", views.PostAddView.as_view(), name="add"),
    path(
        "<int:post_pk>/<int:comment_pk>/delete/",
        views.comment_delete,
        name="comment-delete",
    ),
    path("<int:pk>/", include(postpatterns)),
]
