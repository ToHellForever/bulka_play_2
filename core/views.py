from django.shortcuts import render, redirect
from django.views.generic import TemplateView, View
import random
from django.contrib import messages
from .models import Product, Arenda, News, Order, PlayerRange, Size, PlayerCount, PlayerAge, GameType, AdditionalProducts


class LandingView(TemplateView):
    template_name = "landing.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["products"] = Product.objects.filter(is_active=True).order_by("-created_at")
        context["active_product_count"] = Product.objects.filter(is_active=True).count()
        context["arenda"] = Arenda.objects.filter(is_active=True).order_by("-created_at")
        context["additional_products"] = AdditionalProducts.objects.filter(is_active=True).order_by("-created_at")
        return context
    