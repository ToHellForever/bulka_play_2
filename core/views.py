from django.shortcuts import render, redirect
from django.views.generic import TemplateView, View
from django.http import JsonResponse
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.utils import timezone
from datetime import timedelta
import re
import logging
from django.db import transaction
from django.db.models import Max
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

logger = logging.getLogger(__name__)


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

        # Get the active discount
        from datetime import datetime
        active_discount = Discount.objects.filter(
            is_active=True,
            start_date__lte=datetime.now().date(),
            end_date__gte=datetime.now().date()
        ).first()

        # Add the active discount to the context
        context["active_discount"] = active_discount

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
        ).order_by("order", "-created_at")
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
            products = products.order_by("order", "-created_at")

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

        # Оставляем существующий список продуктов без изменений
        context["products"] = Product.objects.filter(is_active=True).order_by("-created_at")

        # Добавляем новый список продуктов для блока "СМОТРИТЕ ТАКЖЕ", исключая текущий продукт
        context["similar_products"] = Product.objects.filter(is_active=True).exclude(pk=current_product.pk).order_by("-created_at")

        context["additional_images"] = current_product.additional_images.all()

        # Добавьте передачу данных аренды
        context["arenda"] = Arenda.objects.filter(is_active=True).order_by("-created_at")
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
        context["products"] = Product.objects.filter(is_active=True).order_by("-created_at")
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
        # Список дополнительных продуктов, исключая текущий
        context["similar_additional_products"] = AdditionalProducts.objects.filter(
            is_active=True
        ).exclude(pk=current_additional_product.pk).order_by("-created_at")
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

        # Получаем максимальное значение max_players из всех записей PlayerRange
        max_players = PlayerRange.objects.aggregate(Max('max_players'))['max_players__max']
        context["max_players"] = max_players if max_players is not None else 25

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
            ip_address = self.get_client_ip(request)
            
            # ЛОГИРОВАНИЕ: что пришло от пользователя
            print("=" * 60)
            print(f"=== ПРОИСХОДИТ ЗАПРОС НА СОЗДАНИЕ ЗАКАЗА ===")
            print(f"POST data keys: {list(data.keys())}")
            print(f"name: {data.get('name')}")
            print(f"phone: {data.get('phone')}")
            print(f"order_type: {data.get('order_type')}")
            print(f"comment: {data.get('comment')}")
            print(f"delivery_address (RAW): '{data.get('delivery_address')}' repr={repr(data.get('delivery_address'))}")
            print(f"rent_address (RAW): '{data.get('rent_address')}' repr={repr(data.get('rent_address'))}")
            print(f"double_game_count: {data.get('double_game_count', 1)}")
            print("=" * 60)

            # Проверка времени между заявками с одного IP
            # recent_orders = Order.objects.filter(ip_address=ip_address).order_by('-created_at')[:3]
            # if recent_orders.count() >= 3:
            #     last_order = recent_orders.first()
            #     cooldown_period = timedelta(minutes=30)  # Ограничение: 30 минут после 3 заявок
            #     time_since_last_order = timezone.now() - last_order.created_at
            #     if time_since_last_order < cooldown_period:
            #         return JsonResponse(
            #             {
            #                 "success": False,
            #                 "message": f"Вы отправили 3 заявки подряд. Пожалуйста, подождите {cooldown_period.seconds//60 - time_since_last_order.seconds//60} минут перед отправкой следующей заявки.",
            #             },
            #             status=400,
            #         )

            # Проверка комментария на наличие ссылок и спама
            comment = data.get("comment_buy", "") or data.get("comment_rent", "")
            if self.is_spam_comment(comment):
                return JsonResponse(
                    {
                        "success": False,
                        "message": "Ваш комментарий содержит запрещенные символы или ссылки. Пожалуйста, удалите их и попробуйте снова.",
                    },
                    status=400,
                )

            # Определение адреса доставки ДО создания заказа
            delivery_address = None
            if data.get("order_type") in ("buy", "double_buy"):
                delivery_address = data.get("delivery_address")
            elif data.get("order_type") == "rent":
                delivery_address = data.get("rent_address")
            
            # Создание заказа и установка M2M-связей в одной транзакции,
            # чтобы email-уведомление (через transaction.on_commit) ушло
            # только после того, как все товары сохранены
            with transaction.atomic():
                order = Order.objects.create(
                    name=data.get("name"),
                    phone=data.get("phone"),
                    order_type=data.get("order_type"),
                    comment=comment,
                    double_game_count=data.get("double_game_count", 1),
                    ip_address=ip_address,
                    delivery_address=delivery_address,
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

                # Сохраняем изменения полей (engraving, date и т.д.)
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

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def is_spam_comment(self, comment):
        # Проверка на наличие ссылок
        url_pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
        if url_pattern.search(comment):
            return True

        # Проверка на наличие спам-слов (можно расширить список)
        spam_keywords = ['реклама', 'купить', 'дешево', 'скидка', 'бесплатно', 'заработок']
        for keyword in spam_keywords:
            if keyword in comment.lower():
                return True

        return False


class PrivacyPolicyView(TemplateView):
    template_name = 'privacy_policy.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class OfferView(TemplateView):
    template_name = 'public_offer.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context