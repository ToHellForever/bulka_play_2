from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from core.models import Product, Arenda, News, AdditionalProducts


class ProductSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.9

    def items(self):
        return Product.objects.filter(is_active=True, slug__isnull=False)

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        try:
            return obj.get_absolute_url()
        except AttributeError:
            return ""  # Возвращаем пустую строку, если ссылка отсутствует


class ArendaSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Arenda.objects.filter(is_active=True, slug__isnull=False)

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
        return News.objects.filter(is_active=True, slug__isnull=False)

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        try:
            return obj.get_absolute_url()
        except AttributeError:
            return ""


class AdditionalProductsSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.6

    def items(self):
        return AdditionalProducts.objects.filter(is_active=True, slug__isnull=False)

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        try:
            return obj.get_absolute_url()
        except AttributeError:
            return ""


class StaticViewSitemap(Sitemap):
    # Меняем приоритет и частоту обновления
    priority = 0.5
    changefreq = "monthly"

    def items(self):
        # Список URL, которые соответствуют вашим статичным страницам
        return ["landing", "about", "game_catalog", "rental_catalog"]

    def location(self, item):
        # Используем reverse для получения URL страницы
        return reverse(item)
