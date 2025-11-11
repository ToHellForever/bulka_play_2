from django.contrib import admin
from .models import (
    Product, Arenda, Order, News, ProductImage,
    Size, PlayerCount, GameType, PlayerAge, NewsImage, PlayerRange, AdditionalProducts, AdditionalProductsImage, GameKitItem
)
admin.site.register(ProductImage)
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1  # Количество дополнительных форм для новых изображений

admin.site.register(NewsImage)
class NewsImageInline(admin.TabularInline):
    model = NewsImage
    extra = 1 

admin.site.register(AdditionalProductsImage)
class AdditionalProductsImageInline(admin.TabularInline):
    model = AdditionalProductsImage
    extra = 1 
    
# Основной класс для регистрации модели Product
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'is_active', 'created_at')
    list_editable = ('is_active',)
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'description')
    filter_horizontal = ('sizes', 'player_counts', 'game_types', 'player_ages')

    fieldsets = (
        ("Основные поля", {
            'fields': ('name', 'description', 'price', 'image'),
        }),
        ("Атрибуты", {
            'fields': ('sizes', 'player_counts', 'game_types', 'player_ages', 'game_rules', 'game_kit_items', 'additional_info'),
        }),
        ("Дополнительно", {
            'fields': ('is_active',),
        })
    )

    # Указываем созданный inline-класс
    inlines = [
        ProductImageInline,
    ]
    
@admin.register(GameKitItem)
class GameKitItemAdmin(admin.ModelAdmin):
    list_display = ('highlighted_text', 'normal_text')
    search_fields = ('highlighted_text', 'normal_text', 'description')
    
    def full_item(self, obj):
        """
        Для более удобного просмотра полных элементов комплектации в админке
        """
        return f"{obj.highlighted_text} {obj.normal_text}"
    full_item.short_description = "Полный элемент"
@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(PlayerCount)
class PlayerCountAdmin(admin.ModelAdmin):
    list_display = ('count',)
    search_fields = ('count',)

@admin.register(GameType)
class GameTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(PlayerAge)
class PlayerAgeAdmin(admin.ModelAdmin):
    list_display = ('age',)
    search_fields = ('age',)
    
    
class RangeInline(admin.TabularInline):
    model = Arenda.ranges.through
    extra = 1

@admin.register(Arenda)
class ArendaAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'is_active', 'created_at')
    list_editable = ('is_active',)
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'description')
    inlines = [RangeInline]

@admin.register(PlayerRange)
class PlayerRangeAdmin(admin.ModelAdmin):
    list_display = ('min_players', 'max_players', 'min_game_count', 'max_game_count')
    search_fields = ('min_players', 'max_players')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'order_type', 'created_at', 'get_products', 'get_games_for_rent')
    list_filter = ('order_type', 'created_at')
    search_fields = ('name', 'phone', 'comment')

    def get_products(self, obj):
        return ", ".join([p.name for p in obj.products.all()])
    get_products.short_description = "Выбранные товары"
    
    def get_games_for_rent(self, obj):
        return ", ".join([g.name for g in obj.games_for_rent.all()])
    get_games_for_rent.short_description = "Игры для аренды"

    

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'created_at')
    list_editable = ('is_active',)
    
    fieldsets = (
        ("Основные поля", {
            'fields': ('name', 'image'),
        }),
    )
    # Указываем созданный inline-класс
    inlines = [
        NewsImageInline,
    ]

@admin.register(AdditionalProducts)
class AdditionalProducts(admin.ModelAdmin):
    list_display = ('name', 'price', 'is_active', 'created_at')
    list_editable = ('is_active',)
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'description')
    fieldsets = (
        ("Основные поля", {
            'fields': ('name', 'description', 'price', 'image'),
        }),
        ("Дополнительно", {
            'fields': ('is_active',),
        })
    )
    inlines = [
        AdditionalProductsImageInline,
    ]