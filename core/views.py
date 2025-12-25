from django.shortcuts import render, redirect
from django.views.generic import TemplateView, View
from django.http import JsonResponse
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import (
    Product,
    Arenda,
    News,
    Order,
    PlayerRange,
    Size,
    PlayerCount,
    PlayerAge,
    GameType,
    AdditionalProducts,
    Discount,
)


class LandingView(TemplateView):
    template_name = "landing.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["products"] = Product.objects.filter(is_active=True).order_by(
            "-created_at"
        )
        context["active_product_count"] = Product.objects.filter(is_active=True).count()
        context["arenda"] = Arenda.objects.filter(is_active=True).order_by(
            "-created_at"
        )
        context["additional_products"] = AdditionalProducts.objects.filter(
            is_active=True
        ).order_by("-created_at")
        return context


class AboutView(TemplateView):
    template_name = "about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["products"] = Product.objects.filter(is_active=True).order_by(
            "-created_at"
        )
        context["additional_products"] = AdditionalProducts.objects.filter(
            is_active=True
        ).order_by("-created_at")
        context["arenda"] = Arenda.objects.filter(is_active=True).order_by(
            "-created_at"
        )
        context["news"] = News.objects.filter(is_active=True).order_by("-created_at")
        return context


class GameCatalogView(TemplateView):
    template_name = "game_catalog.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products = Product.objects.filter(is_active=True)
        context["additional_products"] = AdditionalProducts.objects.filter(
            is_active=True
        ).order_by("-created_at")
        context["arenda"] = Arenda.objects.filter(is_active=True).order_by(
            "-created_at"
        )
        # Получаем все возможные значения для фильтров
        sizes = Size.objects.all()
        player_counts = PlayerCount.objects.all()
        player_ages = PlayerAge.objects.all()
        game_types = GameType.objects.all()

        # Обработка поискового запроса
        search_query = self.request.GET.get("search", "")
        if search_query:
            from django.db.models import Q
            products = products.filter(
                Q(name__icontains=search_query) |
                Q(name__icontains=search_query.capitalize()) |
                Q(name__icontains=search_query.upper()) |
                Q(name__icontains=search_query.lower())
            )

        # Обработка фильтров
        if "size" in self.request.GET and self.request.GET["size"]:
            products = products.filter(sizes__name=self.request.GET["size"])

        if "players" in self.request.GET and self.request.GET["players"]:
            products = products.filter(
                player_counts__count=self.request.GET["players"]
            )

        if "age" in self.request.GET and self.request.GET["age"]:
            products = products.filter(player_ages__age=self.request.GET["age"])

        if "type" in self.request.GET and self.request.GET["type"]:
            products = products.filter(game_types__name=self.request.GET["type"])

        # Обработка сортировки
        sort = self.request.GET.get("sort", "")
        if sort == "price_asc":
            products = products.order_by("price")
        elif sort == "price_desc":
            products = products.order_by("-price")
        elif sort == "name_asc":
            products = products.order_by("name")
        elif sort == "name_desc":
            products = products.order_by("-name")
        else:
            products = products.order_by("-created_at")

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
        context["products"] = Product.objects.filter(is_active=True).order_by(
            "-created_at"
        )
        context["additional_images"] = current_product.additional_images.all()

        # Добавьте передачу данных аренды
        context["arenda"] = Arenda.objects.filter(is_active=True).order_by(
            "-created_at"
        )
        additional_products = list(
            AdditionalProducts.objects.filter(is_active=True).order_by("-created_at")
        )
        context["additional_products"] = additional_products
        return context

class AdditionalProductsView(TemplateView):
    template_name = "additional_products.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["additional_products"] = AdditionalProducts.objects.filter(
            is_active=True
        ).order_by("-created_at")
        return context

class AdditionalProductDetailView(TemplateView):
    template_name = "additional_product_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["products"] = Product.objects.filter(is_active=True).order_by(
            "-created_at"
        )
        current_additional_product = AdditionalProducts.objects.get(pk=self.kwargs.get("pk"))
        context["additional_product"] = current_additional_product
        context["additional_images"] = current_additional_product.additional_images.all()

        context["arenda"] = Arenda.objects.filter(is_active=True).order_by(
            "-created_at"
        )
        additional_products = list(
            AdditionalProducts.objects.filter(is_active=True).order_by("-created_at")
        )
        context["additional_products"] = additional_products
        return context
class RentalCatalogView(TemplateView):
    template_name = "rental_catalog.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["additional_products"] = AdditionalProducts.objects.filter(
            is_active=True
        ).order_by("-created_at")
        context["products"] = Product.objects.filter(is_active=True).order_by(
            "-created_at"
        )
        context["arenda"] = Arenda.objects.filter(is_active=True).order_by(
            "-created_at"
        )
        context["news"] = News.objects.filter(is_active=True).order_by("-created_at")
        return context

class TwoGamesOnOneBoardView(TemplateView):
    template_name = "two_games_on_one_board.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["arenda"] = Arenda.objects.filter(is_active=True).order_by(
            "-created_at"
        )
        context["products"] = Product.objects.filter(is_active=True).order_by(
            "-created_at"
        )
        context["additional_products"] = AdditionalProducts.objects.filter(
            is_active=True).order_by(
            "-created_at"
        )
        return context
def calculate_games(request):
    guests = int(request.GET.get('guests'))
    try:
        player_range = PlayerRange.objects.filter(min_players__lte=guests, max_players__gte=guests).first()
        
        if player_range is not None:
            data = {'min': player_range.min_game_count, 'max': player_range.max_game_count}
        else:
            data = {'min': None, 'max': None}
            
        return JsonResponse(data)
    
    except Exception as e:
        print(f"Ошибка: {e}")
        return JsonResponse({'error': str(e)}, status=500)
    

@method_decorator(csrf_exempt, name="dispatch")
class ProcessOrderView(View):
    def post(self, request, *args, **kwargs):
        try:
            data = request.POST

            # Создание заказа
            order = Order.objects.create(
                name=data.get("name"),
                phone=data.get("phone"),
                order_type=data.get("order_type"),
                comment=data.get("comment", ""),
                double_game_count=data.get("double_game_count", 1),
            )

            # Обработка в зависимости от типа заказа
            if data.get("order_type") == "buy":
                # Сохранение выбранных игр для покупки
                if "buy_games" in data:
                    games = data.getlist("buy_games")
                    order.products.set(games)

                # Сохранение дополнительных товаров
                if "additional_goods" in data:
                    additional_goods = data.getlist("additional_goods")
                    order.additional_products.set(additional_goods)

                # Сохранение адреса доставки
                order.delivery_address = data.get("delivery_address")

                # Сохранение информации о гравировке
                order.engraving = data.get("engraving", "no")

            elif data.get("order_type") == "double_buy":
                # Сохранение выбранных игр для покупки 2 игр на одной доске
                if "buy_games" in data:
                    games = data.getlist("buy_games")
                    order.products.set(games)

                # Сохранение дополнительных товаров
                if "additional_goods" in data:
                    additional_goods = data.getlist("additional_goods")
                    order.additional_products.set(additional_goods)

                # Сохранение адреса доставки
                order.delivery_address = data.get("delivery_address")

                # Сохранение информации о гравировке
                order.engraving = data.get("engraving", "no")

                # Установка количества игр на одной доске
                order.double_game_count = 2

            elif data.get("order_type") == "rent":
                # Сохранение выбранных игр для аренды
                if "rent_games" in data:
                    games = data.getlist("rent_games")
                    order.games_for_rent.set(games)

                # Сохранение типа аренды
                if "rent_type" in data:
                    order.arenda.set([data.get("rent_type")])

                # Сохранение даты аренды
                if "rent_date" in data:
                    order.date = data.get("rent_date")

                # Сохранение адреса доставки
                order.delivery_address = data.get("rent_address")

            order.save()

            return JsonResponse({"success": True, "message": "Заказ успешно оформлен!"})

        except Exception as e:
            return JsonResponse(
                {
                    "success": False,
                    "message": f"Ошибка при оформлении заказа: {str(e)}",
                },
                status=400,
            )
