from django.urls import path
from . import views

app_name = "posts"

urlpatterns = [
    path("", views.PostListView.as_view(), name="home"),
    path("add/", views.PostAddView.as_view(), name="add"),
    path("<int:pk>/", views.PostDetailView.as_view(), name="detail"),
    path("<int:pk>/delete/", views.post_delete, name="delete"),
    path("<int:pk>/edit/", views.PostEditView.as_view(), name="edit"),
]
