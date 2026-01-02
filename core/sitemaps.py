from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from core.models import Product, Arenda, News, AdditionalProducts


class ProductSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.9

    def items(self):
        return Product.objects.filter(is_published=True, slug__isnull=False)

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        try:
            return obj.get_absolute_url()
        except AttributeError:
            return ""


class ArendaSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Arenda.objects.filter(is_published=True, slug__isnull=False)

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        try:
            return obj.get_absolute_url()
        except AttributeError:
            return ""


class NewsSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.7

    def items(self):
        return News.objects.filter(is_published=True, slug__isnull=False)

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        if obj is None:
            return ""
        return obj.get_absolute_url()


class AdditionalProductsSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.6

    def items(self):
        return AdditionalProducts.objects.filter(is_published=True, slug__isnull=False)

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        try:
            return obj.get_absolute_url()
        except AttributeError:
            return ""


class StaticViewSitemap(Sitemap):
    # Приоритет для статичных страниц, обычно ниже, чем у динамического контента
    priority = 0.5
    # Частота изменения для статичных страниц, обычно реже
    changefreq = "monthly"

    def items(self):
        # Метод возвращает список имен URL-адресов, определенных в urls.py
        # для статичных страниц.
        return [
            "landing",
            "about",
            "game_catalog",
            "rental_catalog",
            "two_games_on_one_board",
        ]

    def location(self, item):
        # Для статичных страниц используем функцию reverse для получения URL
        # по их имени, определенному в urls.py.
        return reverse(item)
