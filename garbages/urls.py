from django.urls import path
from . import views

app_name = "garbages"

urlpatterns = [
    path("", views.GarbageListView.as_view(), name="list"),
    path("<int:pk>/", views.GarbageDetailView.as_view(), name="detail"),
    path("<int:pk>/delete/", views.delete_garbage, name="delete"),
    path("<int:pk>/update/", views.GarbageEditView.as_view(), name="update"),
    path("add/", views.GarbageAddView.as_view(), name="add"),
]
