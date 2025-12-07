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
    highlighted_text = models.CharField(
        max_length=50,
        verbose_name="Выделенный текст",
        help_text="Текст, который будет отображаться крупным шрифтом (например, '46x46см')",
    )
    normal_text = models.CharField(
        max_length=200,
        verbose_name="Обычный текст",
        help_text="Текст, который будет отображаться обычным шрифтом (например, 'игровое поле')",
    )

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
        related_name='products',
    )

    # Правила игры
    game_rules = models.TextField(
        verbose_name="Правила игры",
        blank=True,
        null=True,
        help_text="Введите правила игры. Каждый новый пункт будет отображаться с новой строки.",
    )

    # Дополнительная информация
    additional_info = models.TextField(
        verbose_name="Дополнительно",
        blank=True,
        null=True,
        help_text="Введите дополнительную информацию. Каждый новый пункт будет отображаться с новой строки.",
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

    def get_discounted_price(self):
        """Возвращает цену товара с учетом активных скидок"""
        active_discounts = self.discounts.filter(
            is_active=True,
            start_date__lte=datetime.now().date(),
            end_date__gte=datetime.now().date()
        )

        if not active_discounts.exists():
            return self.price

        # Применяем самую выгодную скидку
        best_price = self.price

        for discount in active_discounts:
            discounted_price = discount.apply_discount(self.price)
            if discounted_price < best_price:
                best_price = discounted_price

        return best_price

class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='additional_images',
        verbose_name="Товар",
    )
    image = models.ImageField(
        upload_to='product_images/additional/',
        verbose_name="Дополнительное изображение",
    )
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
    CARD_STYLE_CHOICES = [
        (1, 'Стиль 1 (оранжевый)'),
        (2, 'Стиль 2 (альтернативный)'),
    ]

    name = models.CharField(max_length=200, verbose_name="Название аренды")
    game_count = models.PositiveIntegerField(verbose_name="Количество игр в аренде", default=6)
    description = models.TextField(verbose_name="Описание")
    time = models.CharField(verbose_name="Время в часах", default=2)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    image = models.ImageField(upload_to='products/', verbose_name="Изображение")
    card_style = models.PositiveSmallIntegerField(
        verbose_name="Стиль карточки",
        choices=CARD_STYLE_CHOICES,
        default=1
    )
    ranges = models.ManyToManyField(PlayerRange, verbose_name="Диапазоны игроков и игр", blank=True)
    is_active = models.BooleanField(default=True, verbose_name="Отображать на сайте")
    is_specific_game = models.BooleanField(default=False, verbose_name="Аренда конкретной игры")
    specific_game = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Аренда"
        verbose_name_plural = "Аренды"
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def get_discounted_price(self):
        """Возвращает цену аренды с учетом активных скидок"""
        active_discounts = self.discounts.filter(
            is_active=True,
            start_date__lte=datetime.now().date(),
            end_date__gte=datetime.now().date()
        )

        if not active_discounts.exists():
            return self.price

        # Применяем самую выгодную скидку
        best_price = self.price

        for discount in active_discounts:
            discounted_price = discount.apply_discount(self.price)
            if discounted_price < best_price:
                best_price = discounted_price

        return best_price

    def get_time_in_hours(self):
        """Возвращает время аренды в часах"""
        return self.time // 60

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
    image = models.ImageField(
        upload_to='news_images/additional/', verbose_name="Дополнительное изображение"
    )
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

    def __str__(self):
        return self.name

    def get_discounted_price(self):
        """Возвращает цену дополнительного товара с учетом активных скидок"""
        active_discounts = self.discounts.filter(
            is_active=True,
            start_date__lte=datetime.now().date(),
            end_date__gte=datetime.now().date()
        )

        if not active_discounts.exists():
            return self.price

        # Применяем самую выгодную скидку
        best_price = self.price

        for discount in active_discounts:
            discounted_price = discount.apply_discount(self.price)
            if discounted_price < best_price:
                best_price = discounted_price

        return best_price

class AdditionalProductsImage(models.Model):
    additional_product = models.ForeignKey(
        AdditionalProducts,
        on_delete=models.CASCADE,
        related_name='additional_images',
        verbose_name="Допы к товару",
    )
    image = models.ImageField(
        upload_to='additional_product_images/additional/',
        verbose_name="Дополнительное изображение",
    )
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
    order_type = models.CharField(
        max_length=10,
        choices=[('buy', 'Купить'), ('rent', 'Аренда'), ('double_buy', 'Купить 2 игры на одной доске')],
        verbose_name="Тип заказа",
    )
    products = models.ManyToManyField(
        Product,
        blank=True,
        verbose_name="Выбранные товары",
        related_name='order_products',
    )
    additional_products = models.ManyToManyField(
        AdditionalProducts,
        blank=True,
        verbose_name="Дополнительные товары",
        related_name='order_additional_products',
    )
    arenda = models.ManyToManyField(
        Arenda, blank=True, verbose_name="Выбранные аренды", related_name='order_arenda'
    )
    games_for_rent = models.ManyToManyField(
        Product,
        blank=True,
        verbose_name="Игры для аренды",
        related_name='order_games_for_rent',
    )
    date = models.DateField(verbose_name="Дата заказа", default=datetime.now)
    time = models.TimeField(verbose_name="Время заказа", default=datetime.now)
    comment = models.TextField(blank=True, verbose_name="Комментарий")
    delivery_address = models.CharField(
        max_length=255, verbose_name="Адрес доставки", blank=True, null=True
    )
    engraving = models.CharField(
        max_length=3,
        choices=[('yes', 'Да'), ('no', 'Нет')],
        default='no',
        verbose_name="Гравировка",
    )
    double_game_count = models.PositiveSmallIntegerField(
        verbose_name="Количество игр на одной доске",
        choices=[(1, '1 игра'), (2, '2 игры')],
        default=1,
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def __str__(self):
        return f"Заказ от {self.name} ({self.created_at})"

    def get_total_price(self):
        """Возвращает общую сумму заказа с учетом скидок"""
        total = 0

        # Товары
        for product in self.products.all():
            # Если выбрано 2 игры на одной доске, то цена за каждую игру уменьшается на 10%
            if self.double_game_count == 2:
                total += product.get_discounted_price() * 0.9 * 2
            else:
                total += product.get_discounted_price()

        # Дополнительные товары
        for additional_product in self.additional_products.all():
            total += additional_product.get_discounted_price()

        # Аренды
        for arenda in self.arenda.all():
            total += arenda.get_discounted_price()

        # Игры для аренды
        for game in self.games_for_rent.all():
            total += game.get_discounted_price()

        return total

class OrderedGameKitItem(models.Model):
    product = models.ForeignKey(
        'Product', on_delete=models.CASCADE, related_name='ordered_game_kits'
    )
    game_kit_item = models.ForeignKey('GameKitItem', on_delete=models.CASCADE)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

class DiscountType(models.TextChoices):
    PERCENTAGE = 'percentage', 'Процентная'
    FIXED = 'fixed', 'Фиксированная'

class Discount(models.Model):
    """Модель скидки"""
    name = models.CharField(max_length=200, verbose_name="Название скидки")
    discount_type = models.CharField(
        max_length=10,
        choices=DiscountType.choices,
        default=DiscountType.PERCENTAGE,
        verbose_name="Тип скидки"
    )
    value = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Значение скидки")
    start_date = models.DateField(verbose_name="Дата начала действия")
    end_date = models.DateField(verbose_name="Дата окончания действия")
    is_active = models.BooleanField(default=True, verbose_name="Активна")
    products = models.ManyToManyField(
        Product,
        blank=True,
        verbose_name="Товары",
        related_name='discounts'
    )
    arendas = models.ManyToManyField(
        Arenda,
        blank=True,
        verbose_name="Аренды",
        related_name='discounts'
    )
    additional_products = models.ManyToManyField(
        AdditionalProducts,
        blank=True,
        verbose_name="Дополнительные товары",
        related_name='discounts',
    )

    class Meta:
        verbose_name = "Скидка"
        verbose_name_plural = "Скидки"
        ordering = ['-start_date']

    def __str__(self):
        return f"{self.name} ({self.get_discount_type_display()}: {self.value})"

    def apply_discount(self, original_price):
        """Применяет скидку к оригинальной цене"""
        if not self.is_active:
            return original_price

        today = datetime.now().date()
        if not (self.start_date <= today <= self.end_date):
            return original_price

        if self.discount_type == DiscountType.PERCENTAGE:
            return original_price * (1 - self.value / 100)
        else:  # FIXED
            return max(original_price - self.value, 0)
