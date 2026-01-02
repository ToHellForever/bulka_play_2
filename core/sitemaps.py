from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from django.conf import settings
from core.models import Product, Arenda, News

class ProductSitemap(Sitemap):
    # Частота изменения страницы: "weekly" (еженедельно), "daily" (ежедневно) и т.д.
    changefreq = "weekly"
    # Приоритет страницы относительно других страниц на сайте (от 0.0 до 1.0)
    priority = 0.9

    def items(self):
        # Метод возвращает QuerySet объектов, для которых будут сгенерированы URL
        # В данном случае, это активные товары
        return Product.objects.filter(is_active=True)

    def lastmod(self, obj):
        # Метод возвращает дату последнего изменения объекта.
        # Используется для информирования поисковиков об актуальности контента.
        return obj.updated_at

    def location(self, obj):
        # Метод возвращает абсолютный URL для каждого объекта.
        return reverse('product_detail', kwargs={'pk': obj.pk})

class ArendaSitemap(Sitemap):
    # Частота изменения страницы: "weekly" (еженедельно), "daily" (ежедневно) и т.д.
    changefreq = "weekly"
    # Приоритет страницы относительно других страниц на сайте (от 0.0 до 1.0)
    priority = 0.9

    def items(self):
        # Метод возвращает QuerySet объектов, для которых будут сгенерированы URL
        # В данном случае, это активные аренды
        return Arenda.objects.filter(is_active=True)

    def lastmod(self, obj):
        # Метод возвращает дату последнего изменения объекта.
        # Используется для информирования поисковиков об актуальности контента.
        return obj.updated_at if hasattr(obj, 'updated_at') else None

    def location(self, obj):
        # Метод возвращает абсолютный URL для каждого объекта.
        # Для аренды нет отдельной страницы, поэтому возвращаем URL каталога аренд
        return reverse('rental_catalog')

class NewsSitemap(Sitemap):
    # Частота изменения страницы: "weekly" (еженедельно), "daily" (ежедневно) и т.д.
    changefreq = "weekly"
    # Приоритет страницы относительно других страниц на сайте (от 0.0 до 1.0)
    priority = 0.8

    def items(self):
        # Метод возвращает QuerySet объектов, для которых будут сгенерированы URL
        # В данном случае, это активные новости
        return News.objects.filter(is_active=True)

    def lastmod(self, obj):
        # Метод возвращает дату последнего изменения объекта.
        # Используется для информирования поисковиков об актуальности контента.
        return obj.updated_at if hasattr(obj, 'updated_at') else None

    def location(self, obj):
        # Метод возвращает абсолютный URL для каждого объекта.
        # Новости отображаются на главной странице, поэтому возвращаем URL главной
        return reverse('landing')

class StaticViewSitemap(Sitemap):
    # Приоритет для статичных страниц, обычно ниже, чем у динамического контента
    priority = 0.5
    # Частота изменения для статичных страниц, обычно реже
    changefreq = "monthly"

    def items(self):
        # Метод возвращает список имен URL-адресов, определенных в urls.py
        # для статичных страниц.
        return ['landing', 'about', 'game_catalog', 'rental_catalog', 'two_games_on_one_board']

    def location(self, item):
        # Для статичных страниц используем функцию reverse для получения URL
        # по их имени, определенному в urls.py.
        return reverse(item)
