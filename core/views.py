from django.shortcuts import render, redirect
from django.views.generic import TemplateView, View
from django.http import JsonResponse
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
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
        current_product = Product.objects.get(pk=self.kwargs.get("pk"))
        context["product"] = current_product
        context["products"] = Product.objects.filter(is_active=True).order_by("-created_at")
        context["additional_images"] = current_product.additional_images.all()

        random_products = list(Product.objects.filter(is_active=True).exclude(pk=current_product.pk).order_by('?')[:4]) 
        context["random_products"] = random_products 

        additional_products = list(AdditionalProducts.objects.filter(is_active=True).order_by('-created_at'))
        context["additional_products"] = additional_products
        return context
    
    
class RentalCatalogView(TemplateView):
    template_name = "rental_catalog.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["arenda"] = Arenda.objects.filter(is_active=True).order_by("-created_at")
        context["news"] = News.objects.filter(is_active=True).order_by("-created_at")
        return context

@method_decorator(csrf_exempt, name='dispatch')
class ProcessOrderView(View):
    def post(self, request, *args, **kwargs):
        try:
            data = request.POST

            # Создание заказа
            order = Order.objects.create(
                name=data.get('name'),
                phone=data.get('phone'),
                order_type=data.get('order_type'),
                comment=data.get('comment', '')
            )

            # Обработка в зависимости от типа заказа
            if data.get('order_type') == 'buy':
                # Сохранение выбранных игр для покупки
                if 'buy_games' in data:
                    games = data.getlist('buy_games')
                    order.products.set(games)

                # Сохранение дополнительных товаров
                if 'additional_goods' in data:
                    additional_goods = data.getlist('additional_goods')
                    order.additional_products.set(additional_goods)

                # Сохранение адреса доставки
                order.delivery_address = data.get('delivery_address')

                # Сохранение информации о гравировке
                order.engraving = data.get('engraving', 'no')

            elif data.get('order_type') == 'rent':
                # Сохранение выбранных игр для аренды
                if 'rent_games' in data:
                    games = data.getlist('rent_games')
                    order.games_for_rent.set(games)

                # Сохранение типа аренды
                if 'rent_type' in data:
                    order.arenda.set([data.get('rent_type')])

                # Сохранение даты аренды
                if 'rent_date' in data:
                    order.date = data.get('rent_date')

                # Сохранение адреса доставки
                order.delivery_address = data.get('rent_address')

            order.save()

            return JsonResponse({
                'success': True,
                'message': 'Заказ успешно оформлен!'
            })

        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Ошибка при оформлении заказа: {str(e)}'
            }, status=400)
