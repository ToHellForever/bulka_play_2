from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.db import transaction
from django.db.models import Q
from .models import Order
from .email_service import send_email_notification
from django.conf import settings
import logging

# Настраиваем логгер для записи в файл
logger = logging.getLogger("core")
logger.setLevel(logging.DEBUG)

# Handler для файла
file_handler = logging.FileHandler('core_signals.log', encoding='utf-8')
file_handler.setLevel(logging.DEBUG)
file_formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)

# Handler для консоли
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_formatter = logging.Formatter('%(levelname)s: %(message)s')
console_handler.setFormatter(console_formatter)
logger.addHandler(console_handler)


def send_email_notification_for_order(instance):
    """Отправка email уведомления о новом заказе"""
    try:
        # Формируем список товаров
        products_list = [product.name for product in instance.products.all()]
        additional_products_list = [
            product.name for product in instance.additional_products.all()
        ]

        logger.info(f"Order {instance.id} arenda relations: {instance.arenda.all()}")

        arenda_list = [arenda.name for arenda in instance.arenda.all()]
        games_for_rent_list = [game.name for game in instance.games_for_rent.all()]

        # Формируем список игр для 2 в 1, если это соответствующий тип заказа
        double_buy_games_list = []
        if instance.order_type == 'double_buy' and products_list:
            double_buy_games_list = products_list.copy()

        # Формируем адрес доставки (проверяем и пустую строку, и None)
        logger.info(f"Order {instance.id} BEFORE delivery_address check: raw='{instance.delivery_address}' repr={repr(instance.delivery_address)}")
        delivery_address = instance.delivery_address if instance.delivery_address else "Не указан"
        logger.info(f"Order {instance.id} AFTER delivery_address check: resolved='{delivery_address}'")

        # Формируем сообщение
        email_message = f"""
📦 Новый заказ! 📦

👤 Имя: {instance.name}
📞 Телефон: {instance.phone}
📋 Тип заказа: {instance.get_order_type_display()}
📅 Дата заказа: {instance.date.strftime("%d.%m.%Y") if instance.date else "Не указана"}
⏰ Время заказа: {instance.time.strftime("%H:%M") if instance.time else "Не указано"}

🎮 Товары: {', '.join(products_list) if products_list else "Нет"}
🎮 Дополнительные товары: {', '.join(additional_products_list) if additional_products_list else "Нет"}
🎮 Аренды: {', '.join(arenda_list) if arenda_list else "Нет"}
🎮 Игры для аренды: {', '.join(games_for_rent_list) if games_for_rent_list else "Нет"}
🎮 Игры для 2 в 1: {', '.join(double_buy_games_list) if double_buy_games_list else "Нет"}

💬 Комментарий: {instance.comment if instance.comment else "Нет"}

📍 Адрес доставки: {delivery_address}

🔗 Подробнее: http://bulka-play.ru/s3cr3t_4dm1n_bulk4_pl4y2_p4th/core/order/{instance.id}/change/
        """

        logger.info(f"Order {instance.id} email_message length: {len(email_message)}")
        logger.info(f"Order {instance.id} email_message preview:\n{email_message[:500]}")

        # Отправляем email уведомление
        success = send_email_notification(
            subject=f"Новый заказ #{instance.id} от {instance.name}",
            message=email_message
        )
        if success:
            logger.info(f"Email успешно отправлен для заказа #{instance.id}")
        else:
            logger.error(f"Не удалось отправить email для заказа #{instance.id}")
    except Exception as e:
        logger.error(f"Ошибка отправки email уведомления: {e}", exc_info=True)


# Флаг для отслеживания того, что email уже был отправлен
_email_sent_for_order = set()


@receiver(post_save, sender=Order)
def notify_email_on_order_created(sender, instance, created, **kwargs):
    """Обработка создания заказа - планируем отправку email"""
    if created:
        logger.info("Order created, scheduling email...")
        transaction.on_commit(lambda: _send_email_if_not_sent(instance))


@receiver(m2m_changed, sender=Order.products.through)
@receiver(m2m_changed, sender=Order.additional_products.through)
@receiver(m2m_changed, sender=Order.arenda.through)
@receiver(m2m_changed, sender=Order.games_for_rent.through)
def notify_email_on_order_m2m_changed(sender, instance, action, **kwargs):
    """Обработка m2m изменений - планируем отправку email, если ещё не запланирована"""
    if action == "post_add" and isinstance(instance, Order):
        logger.info(f"M2M relations changed for order {instance.id}, action: {action}")
        _send_email_if_not_sent(instance)


def _send_email_if_not_sent(instance):
    """Отправить email, если ещё не отправлен и не запланирован"""
    order_id = instance.id
    
    # Если email уже отправлен для этого заказа, ничего не делаем
    if order_id in _email_sent_for_order:
        logger.info(f"Email для заказа #{order_id} уже отправлен, пропускаем")
        return
    
    logger.info(f"Планируем отправку email для заказа #{order_id}")
    
    # Помечаем как отправленный ДО вызова transaction.on_commit
    # Это предотвращает дублирование при нескольких вызовах
    _email_sent_for_order.add(order_id)
    
    # Отправляем email через transaction.on_commit
    transaction.on_commit(lambda: _send_order_email(instance))


def _send_order_email(instance):
    """Отправить email о заказе"""
    order_id = instance.id
    
    try:
        # Загружаем свежие данные из БД (включая delivery_address)
        instance.refresh_from_db()
        
        # Проверяем, что все m2m связи уже установлены
        products_count = instance.products.count()
        additional_count = instance.additional_products.count()
        arenda_count = instance.arenda.count()
        games_count = instance.games_for_rent.count()
        
        logger.info(f"Order {instance.id} - products: {products_count}, additional: {additional_count}, arenda: {arenda_count}, games: {games_count}")
        logger.info(f"Order {instance.id} - delivery_address: '{instance.delivery_address}'")
        
        # Отправляем email
        send_email_notification_for_order(instance)
            
    except Exception as e:
        logger.error(f"Ошибка при отправке email: {e}", exc_info=True)
