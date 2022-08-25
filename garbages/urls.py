from django.urls import path
from . import views

app_name = "garbages"

urlpatterns = [path("/", views.GarbageListView.as_view(), name="list")]
