from django.contrib import admin
from .models import (
    Product,
    Arenda,
    Order,
    News,
    ProductImage,
    Size,
    PlayerCount,
    GameType,
    PlayerAge,
    NewsImage,
    PlayerRange,
    AdditionalProducts,
    AdditionalProductsImage,
    GameKitItem,
    OrderedGameKitItem,
    Discount,
    GameKitItemAdditional,
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


class OrderedGameKitItemInline(admin.TabularInline):
    model = OrderedGameKitItem
    extra = 1
    fields = ("game_kit_item", "order")  # Теперь можем выставлять порядок вручную
    autocomplete_fields = ["game_kit_item"]  # Автодополнение элемента комплекта


# Основной класс для регистрации модели Product
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "is_active", "created_at")
    list_editable = ("is_active",)
    list_filter = ("is_active", "created_at")
    search_fields = ("name", "description")
    filter_horizontal = ("sizes", "player_counts", "game_types", "player_ages")

    fieldsets = (
        (
            "Основные поля",
            {
                "fields": ("name", "description", "price", "image"),
            },
        ),
        (
            "Атрибуты",
            {
                "fields": (
                    "sizes",
                    "player_counts",
                    "game_types",
                    "player_ages",
                    "game_rules",
                    "game_kit_items",
                    "additional_info",
                ),
            },
        ),
        (
            "Дополнительно",
            {
                "fields": ("is_active",),
            },
        ),
    )

    # Указываем созданный inline-класс
    inlines = [
        ProductImageInline,
        OrderedGameKitItemInline,
    ]


@admin.register(GameKitItem)
class GameKitItemAdmin(admin.ModelAdmin):
    list_display = ("highlighted_text", "normal_text")
    search_fields = ("highlighted_text", "normal_text", "description")

    def full_item(self, obj):
        """
        Для более удобного просмотра полных элементов комплектации в админке
        """
        return f"{obj.highlighted_text} {obj.normal_text}"

    full_item.short_description = "Полный элемент"


@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(PlayerCount)
class PlayerCountAdmin(admin.ModelAdmin):
    list_display = ("count",)
    search_fields = ("count",)


@admin.register(GameType)
class GameTypeAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(PlayerAge)
class PlayerAgeAdmin(admin.ModelAdmin):
    list_display = ("age",)
    search_fields = ("age",)


class RangeInline(admin.TabularInline):
    model = Arenda.ranges.through
    extra = 1


@admin.register(Arenda)
class ArendaAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "price",
        "is_active",
        "is_specific_game",
        "specific_game",
        "created_at",
    )
    list_editable = ("is_active", "is_specific_game")
    list_filter = ("is_active", "is_specific_game", "created_at")
    search_fields = ("name", "description")
    inlines = [RangeInline]

    fieldsets = (
        (
            "Основные поля",
            {
                "fields": ("name", "description", "price", "image"),
            },
        ),
        (
            "Конкретная игра",
            {
                "fields": ("is_specific_game", "specific_game"),
                "description": 'Если выбрано "Конкретная игра", укажите игру, которую можно арендовать.',
            },
        ),
        (
            "Дополнительно",
            {
                "fields": ("is_active",),
            },
        ),
    )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "specific_game":
            kwargs["queryset"] = Product.objects.filter(is_active=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(PlayerRange)
class PlayerRangeAdmin(admin.ModelAdmin):
    list_display = ("min_players", "max_players", "min_game_count", "max_game_count")
    search_fields = ("min_players", "max_players")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "phone",
        "order_type",
        "created_at",
        "get_products",
        "get_games_for_rent",
    )
    list_filter = ("order_type", "created_at")
    search_fields = ("name", "phone", "comment")

    def get_products(self, obj):
        return ", ".join([p.name for p in obj.products.all()])

    get_products.short_description = "Выбранные товары"

    def get_games_for_rent(self, obj):
        return ", ".join([g.name for g in obj.games_for_rent.all()])

    get_games_for_rent.short_description = "Игры для аренды"


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active", "created_at")
    list_editable = ("is_active",)

    fieldsets = (
        (
            "Основные поля",
            {
                "fields": ("name", "image"),
            },
        ),
    )
    # Указываем созданный inline-класс
    inlines = [
        NewsImageInline,
    ]


@admin.register(AdditionalProducts)
class AdditionalProductsAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "is_active", "created_at")
    list_editable = ("is_active",)
    list_filter = ("is_active", "created_at")
    search_fields = ("name", "description")
    fieldsets = (
        (
            "Основные поля",
            {
                "fields": (
                    "name",
                    "description",
                    "description_2",
                    "material",
                    "price",
                    "image",
                    "game_kit_items_additional",
                    "price_prefix",  # Добавляем новое поле
                ),
            },
        ),
        (
            "Дополнительно",
            {
                "fields": ("is_active",),
            },
        ),
    )
    inlines = [
        AdditionalProductsImageInline,
    ]


@admin.register(GameKitItemAdditional)
class GameKitItemAdditionalAdmin(admin.ModelAdmin):
    list_display = ("highlighted_text", "normal_text")
    search_fields = ("highlighted_text", "normal_text", "description")

    def full_item(self, obj):
        """
        Для более удобного просмотра полных элементов комплектации в админке
        """
        return f"{obj.highlighted_text} {obj.normal_text}"

    full_item.short_description = "Полный элемент"


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "get_discount_type",
        "value",
        "start_date",
        "end_date",
        "is_active",
    )
    list_editable = ("is_active",)
    list_filter = ("is_active", "discount_type", "start_date", "end_date")
    search_fields = ("name",)
    filter_horizontal = ("products", "arendas", "additional_products")

    fieldsets = (
        (
            "Основные поля",
            {
                "fields": (
                    "name",
                    "discount_type",
                    "value",
                    "start_date",
                    "end_date",
                    "is_active",
                ),
            },
        ),
        (
            "Применение",
            {
                "fields": ("products", "arendas", "additional_products"),
            },
        ),
    )

    def get_discount_type(self, obj):
        return obj.get_discount_type_display()

    get_discount_type.short_description = "Тип скидки"
