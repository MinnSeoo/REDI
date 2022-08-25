from django.views.generic import ListView
from django.shortcuts import render
from . import models


class GarbageListView(ListView):

    model = models.Garbage
    template_name = "garbages/garbage_list.html"

    
