from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from core.views import (
    LandingView,
    AboutView,
    GameCatalogView,
    ProductDetailView,
    RentalCatalogView,
    ProcessOrderView,
    calculate_games,
    TwoGamesOnOneBoardView,
    AdditionalProductsView,
    AdditionalProductDetailView,
)
sitemaps = {
    'products': ProductSitemap,
    'arendas': ArendaSitemap,
    'news': NewsSitemap,
    'static': StaticViewSitemap,
}

# Защита от случайного доступа к админ-панели
# Используется сложный путь для предотвращения случайного входа
admin.site.site_header = "Администрирование Bulka Play 2"
admin.site.site_title = "Bulka Play 2 Admin"
admin.site.index_title = "Панель управления"

# Сложный путь для админ-панели
ADMIN_URL = "s3cr3t_4dm1n_bulk4_pl4y2_p4th"

urlpatterns = [
    path(f"{ADMIN_URL}/", admin.site.urls),
    path("", LandingView.as_view(), name="landing"),
    path("about/", AboutView.as_view(), name="about"),
    path("game-catalog/", GameCatalogView.as_view(), name="game_catalog"),
    path("product/<int:pk>/", ProductDetailView.as_view(), name="product_detail"),
    path("rental-catalog/", RentalCatalogView.as_view(), name="rental_catalog"),
    path(
        "two-games-on-one-board/",
        TwoGamesOnOneBoardView.as_view(),
        name="two_games_on_one_board",
    ),
    path("process_order/", ProcessOrderView.as_view(), name="process_order"),
    path("calculate_games/", calculate_games, name="calculate_games"),
    path(
        "additional_product_detail/<int:pk>/",
        AdditionalProductDetailView.as_view(),
        name="additional_product_detail",
    ),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
