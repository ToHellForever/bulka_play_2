from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from core.views import (
    LandingView,
    AboutView,
    GameCatalogView,
    ProductDetailView,
    RentalCatalogView,
    ProcessOrderView,
    calculate_games,
    TwoGamesOnOneBoardView,
    AdditionalProductsView
)
from debug_toolbar.toolbar import debug_toolbar_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', LandingView.as_view(), name='landing'),
    path('about/', AboutView.as_view(), name='about'),
    path('game-catalog/', GameCatalogView.as_view(), name='game_catalog'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('rental-catalog/', RentalCatalogView.as_view(), name='rental_catalog'),
    path('two-games-on-one-board/', TwoGamesOnOneBoardView.as_view(), name='two_games_on_one_board'),
    path('process_order/', ProcessOrderView.as_view(), name='process_order'),
    path('calculate_games/', calculate_games, name='calculate_games'),
    path('additional_product_detail/<int:pk>/', AdditionalProductsView.as_view(template_name='additional_product_detail.html'), name='additional_product_detail'),
] + debug_toolbar_urls()

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
