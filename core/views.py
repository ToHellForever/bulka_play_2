from django.shortcuts import render, redirect
from django.views.generic import TemplateView, View
import random
from django.contrib import messages



class LandingView(TemplateView):
    template_name = "landing.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context