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

class AboutView(TemplateView):
    template_name = "about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["news"] = News.objects.filter(is_active=True).order_by("-created_at")
        return context
    
    
class GameCatalogView(TemplateView):
    template_name = "game_catalog.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products = Product.objects.filter(is_active=True)
        context["additional_products"] = AdditionalProducts.objects.filter(is_active=True).order_by("-created_at")

        # Получаем все возможные значения для фильтров
        sizes = Size.objects.all()
        player_counts = PlayerCount.objects.all()
        player_ages = PlayerAge.objects.all()
        game_types = GameType.objects.all()

        # Обработка поискового запроса
        search_query = self.request.GET.get('search', '')
        if search_query:
            products = products.filter(name__iregex=r'{}'.format(search_query))

        # Обработка фильтров
        if 'size' in self.request.GET and self.request.GET['size']:
            products = products.filter(sizes__id=self.request.GET['size'])

        if 'player_count' in self.request.GET and self.request.GET['player_count']:
            products = products.filter(player_counts__id=self.request.GET['player_count'])

        if 'player_age' in self.request.GET and self.request.GET['player_age']:
            products = products.filter(player_ages__id=self.request.GET['player_age'])

        if 'game_type' in self.request.GET and self.request.GET['game_type']:
            products = products.filter(game_types__id=self.request.GET['game_type'])

        # Обработка сортировки
        sort = self.request.GET.get('sort', '')
        if sort == 'price_asc':
            products = products.order_by('price')
        elif sort == 'price_desc':
            products = products.order_by('-price')
        elif sort == 'name_asc':
            products = products.order_by('name')
        elif sort == 'name_desc':
            products = products.order_by('-name')
        else:
            products = products.order_by('-created_at')

        context["products"] = products

        # Добавляем значения для фильтров в контекст
        context["sizes"] = sizes
        context["player_counts"] = player_counts
        context["player_ages"] = player_ages
        context["game_types"] = game_types

        return context
    
    
class ProductDetailView(TemplateView):
    template_name = "product_detail.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["product"] = Product.objects.get(pk=self.kwargs.get("pk"))
        context["additional_images"] = context["product"].additional_images.all()
        return context
