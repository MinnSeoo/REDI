from django.urls import path
from . import views

app_name = "garbages"

urlpatterns = [
    path("garbage/", views.GarbageListView.as_view(), name="gb-list"),
    path("garbage/<int:pk>/", views.GarbageDetailView.as_view(), name="gb-detail"),
    path("garbage/<int:pk>/delete/", views.delete_garbage, name="gb-delete"),
    path("garbage/<int:pk>/update/", views.GarbageEditView.as_view(), name="gb-update"),
    path("garbage/add/", views.GarbageAddView.as_view(), name="gb-add"),
    path("replacement/", views.ReplacementListView.as_view(), name="rm-list"),
    path(
        "replacement/<int:pk>/", views.ReplacementDetailView.as_view(), name="rm-detail"
    ),
    path("replacement/<int:pk>/delete/", views.delete_replacement, name="rm-delete"),
    path(
        "replacement/<int:pk>/update/",
        views.ReplacementEditView.as_view(),
        name="rm-update",
    ),
    path("replacement/add/", views.ReplacementAddView.as_view(), name="rm-add"),
]
