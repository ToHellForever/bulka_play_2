from django.db import models
from datetime import datetime

class Size(models.Model):
    name = models.CharField(max_length=100, verbose_name="Размер")

    class Meta:
        verbose_name = "Размер"
        verbose_name_plural = "Размеры"

    def __str__(self):
        return self.name

class PlayerCount(models.Model):
    count = models.PositiveIntegerField(verbose_name="Количество игроков")

    class Meta:
        verbose_name = "Количество игроков"
        verbose_name_plural = "Количество игроков"

    def __str__(self):
        return str(self.count)

class GameType(models.Model):
    name = models.CharField(max_length=100, verbose_name="Вид игры")

    class Meta:
        verbose_name = "Вид игры"
        verbose_name_plural = "Виды игр"

    def __str__(self):
        return self.name

class PlayerAge(models.Model):
    age = models.CharField(max_length=50, verbose_name="Возраст игроков")

    class Meta:
        verbose_name = "Возраст игрока"
        verbose_name_plural = "Возрасты игроков"

    def __str__(self):
        return self.age
    

class GameKitItem(models.Model):
    """Модель элемента комплектации игры чтобы разделить комплектацию на разные блоки"""
    highlighted_text = models.CharField(max_length=50, verbose_name="Выделенный текст", help_text="Текст, который будет отображаться крупным шрифтом (например, '46x46см')")
    normal_text = models.CharField(max_length=200, verbose_name="Обычный текст", help_text="Текст, который будет отображаться обычным шрифтом (например, 'игровое поле')")
    
    class Meta:
        verbose_name = "Элемент комплектации"
        verbose_name_plural = "Элементы комплектации"

    def __str__(self):
        return f"{self.highlighted_text} {self.normal_text}"
    
    
class Product(models.Model):
    """Модель товара"""
    name = models.CharField(max_length=200, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    image = models.ImageField(upload_to='products/', verbose_name="Изображение")
    is_active = models.BooleanField(default=True, verbose_name="Отображать на сайте")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    # Комплект игры как связь с отдельной моделью
    game_kit_items = models.ManyToManyField(
        GameKitItem,
        verbose_name="Элементы комплектации",
        blank=True,
        related_name='products'
    )

    # Правила игры
    game_rules = models.TextField(
        verbose_name="Правила игры",
        blank=True,
        null=True,
        help_text="Введите правила игры. Каждый новый пункт будет отображаться с новой строки."
    )

    # Дополнительная информация
    additional_info = models.TextField(
        verbose_name="Дополнительно",
        blank=True,
        null=True,
        help_text="Введите дополнительную информацию. Каждый новый пункт будет отображаться с новой строки."
    )
    # Связи с атрибутами
    sizes = models.ManyToManyField(Size, verbose_name="Размеры", blank=True)
    player_counts = models.ManyToManyField(PlayerCount, verbose_name="Количество игроков", blank=True)
    game_types = models.ManyToManyField(GameType, verbose_name="Виды игры", blank=True)
    player_ages = models.ManyToManyField(PlayerAge, verbose_name="Возрасты игроков", blank=True)

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        ordering = ['-created_at']

    def __str__(self):
        return self.name

class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='additional_images',
        verbose_name="Товар",
    )
    image = models.ImageField(upload_to='product_images/additional/', verbose_name="Дополнительное изображение")
    is_main = models.BooleanField(default=False, verbose_name="Основное изображение")

    class Meta:
        verbose_name = "Дополнительное изображение товара"
        verbose_name_plural = "Дополнительные изображения товаров"

    def __str__(self):
        return f'Фото {self.product}'

class PlayerRange(models.Model):
    """
    Диапазоны количества игроков и соответствующее количество игр.
    """
    min_players = models.PositiveIntegerField(verbose_name="Минимальное количество игроков")
    max_players = models.PositiveIntegerField(verbose_name="Максимальное количество игроков")
    min_game_count = models.PositiveIntegerField(verbose_name="Минимальное количество игр")
    max_game_count = models.PositiveIntegerField(verbose_name="Максимальное количество игр")

    class Meta:
        verbose_name = "Диапазон игроков"
        verbose_name_plural = "Диапазоны игроков"

    def __str__(self):
        return f'{self.min_players}-{self.max_players}: {self.min_game_count}-{self.max_game_count} игр'

class Arenda(models.Model):
    """Модель аренды"""
    name = models.CharField(max_length=200, verbose_name="Название аренды")
    game_count = models.PositiveIntegerField(verbose_name="Количество игр в аренде", default=6)
    description = models.TextField(verbose_name="Описание")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    image = models.ImageField(upload_to='products/', verbose_name="Изображение")
    ranges = models.ManyToManyField(PlayerRange, verbose_name="Диапазоны игроков и игр", blank=True)
    is_active = models.BooleanField(default=True, verbose_name="Отображать на сайте")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Аренда"
        verbose_name_plural = "Аренды"
        ordering = ['-created_at']

    def __str__(self):
        return self.name

class News(models.Model):
    """Модель новости"""
    name = models.CharField(max_length=200, verbose_name="Название мероприятия")
    image = models.ImageField(upload_to='news/', verbose_name="Изображение")
    is_active = models.BooleanField(default=True, verbose_name="Отображать на сайте")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Новость"
        verbose_name_plural = "Новости"

    def __str__(self):
        return self.name

class NewsImage(models.Model):
    news = models.ForeignKey(
        News,
        on_delete=models.CASCADE,
        related_name='additional_images',
        verbose_name="Новость",
    )
    image = models.ImageField(upload_to='news_images/additional/', verbose_name="Дополнительное изображение")
    is_main = models.BooleanField(default=False, verbose_name="Основное изображение")

    class Meta:
        verbose_name = "Дополнительное изображение новости"
        verbose_name_plural = "Дополнительные изображения новостей"

    def __str__(self):
        return f'Фото {self.news}'

class AdditionalProducts(models.Model):
    """Модель подставки и сумок"""
    name = models.CharField(max_length=200, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    image = models.ImageField(upload_to='products/', verbose_name="Изображение")
    is_active = models.BooleanField(default=True, verbose_name="Отображать на сайте")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Дополнительное к товарам"
        verbose_name_plural = "Дополнительные к товарам"

class AdditionalProductsImage(models.Model):
    additional_product = models.ForeignKey(
        AdditionalProducts,
        on_delete=models.CASCADE,
        related_name='additional_images',
        verbose_name="Допы к товару",
    )
    image = models.ImageField(upload_to='additional_product_images/additional/', verbose_name="Дополнительное изображение")
    is_main = models.BooleanField(default=False, verbose_name="Основное изображение")

    class Meta:
        verbose_name = "Дополнительное изображение допов товара"
        verbose_name_plural = "Дополнительные изображения допов товара"

    def __str__(self):
        return f'Фото {self.additional_product}'

class Order(models.Model):
    """Модель заказа"""
    name = models.CharField(max_length=100, verbose_name="Имя")
    phone = models.CharField(max_length=15, verbose_name="Телефон")
    order_type = models.CharField(max_length=10, choices=[('buy', 'Купить'), ('rent', 'Аренда')], verbose_name="Тип заказа")
    products = models.ManyToManyField(Product, blank=True, verbose_name="Выбранные товары", related_name="order_products")
    additional_products = models.ManyToManyField(AdditionalProducts, blank=True, verbose_name="Дополнительные товары", related_name="order_additional_products")
    arenda = models.ManyToManyField(Arenda, blank=True, verbose_name="Выбранные аренды", related_name="order_arenda")
    games_for_rent = models.ManyToManyField(Product, blank=True, verbose_name="Игры для аренды", related_name="order_games_for_rent")
    date = models.DateField(verbose_name="Дата заказа", default=datetime.now)
    time = models.TimeField(verbose_name="Время заказа", default=datetime.now)
    comment = models.TextField(blank=True, verbose_name="Комментарий")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def __str__(self):
        return f"Заказ от {self.name} ({self.created_at})"


class OrderedGameKitItem(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='ordered_game_kits')
    game_kit_item = models.ForeignKey('GameKitItem', on_delete=models.CASCADE)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']