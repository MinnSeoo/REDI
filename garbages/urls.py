from django.urls import path, include
from . import views

app_name = "garbages"

garbagepatterns = [
    path("", views.GarbageListView.as_view(), name="gb-list"),
    path("<int:pk>/", views.GarbageDetailView.as_view(), name="gb-detail"),
    path("<int:pk>/delete/", views.delete_garbage, name="gb-delete"),
    path("<int:pk>/update/", views.GarbageEditView.as_view(), name="gb-update"),
    path("add/", views.GarbageAddView.as_view(), name="gb-add"),
]

replacementpatterns = [
    path("", views.ReplacementListView.as_view(), name="rm-list"),
    path("<int:pk>/", views.ReplacementDetailView.as_view(), name="rm-detail"),
    path("<int:pk>/delete/", views.delete_replacement, name="rm-delete"),
    path(
        "<int:pk>/update/",
        views.ReplacementEditView.as_view(),
        name="rm-update",
    ),
    path("add/", views.ReplacementAddView.as_view(), name="rm-add"),
]

urlpatterns = [
    path("garbage/", include(garbagepatterns)),
    path("replacement/", include(replacementpatterns)),
]
