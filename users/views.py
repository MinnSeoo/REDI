from django.shortcuts import render
from django.views.generic import TemplateView


class UserHomeView(TemplateView):

    """
    This is a home view for those who are logged in.
    """

    template_name = "users/home.html"
