from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.db import transaction
from .models import Order
from .tg_bot import send_telegram_message
from django.conf import settings
import asyncio

api_key = settings.TELEGRAM_BOT_API_KEY
user_id = settings.TELEGRAM_USER_ID


def send_telegram_notification(instance):
    try:
        # Принудительно загружаем все связи
        instance.refresh_from_db()

        # Формируем список товаров
        products_list = [product.name for product in instance.products.all()]
        additional_products_list = [
            product.name for product in instance.additional_products.all()
        ]

        # Здесь добавляем отладочный вывод
        print(f"Order {instance.id} arenda relations: {instance.arenda.all()}")

        arenda_list = [arenda.name for arenda in instance.arenda.all()]
        games_for_rent_list = [game.name for game in instance.games_for_rent.all()]

        # Формируем список игр для 2 в 1, если это соответствующий тип заказа
        double_buy_games_list = []
        if instance.order_type == 'double_buy' and products_list:
            double_buy_games_list = products_list.copy()

        # Формируем сообщение
        tg_markdown_message = f"""
📦 *Новый заказ!* 📦
👤 **Имя:** {instance.name}
📞 **Телефон:** {instance.phone}
📋 **Тип заказа:** {instance.get_order_type_display()}
📅 **Дата заказа:** {instance.date.strftime("%d.%m.%Y") if instance.date else "Не указана"}
⏰ **Время заказа:** {instance.time.strftime("%H:%M") if instance.time else "Не указано"}

🎮 **Товары:** {', '.join(products_list) if products_list else "Нет"}
🎮 **Дополнительные товары:** {', '.join(additional_products_list) if additional_products_list else "Нет"}
🎮 **Аренды:** {', '.join(arenda_list) if arenda_list else "Нет"}
🎮 **Игры для аренды:** {', '.join(games_for_rent_list) if games_for_rent_list else "Нет"}
🎮 **Игры для 2 в 1:** {', '.join(double_buy_games_list) if double_buy_games_list else "Нет"}

💬 **Комментарий:** {instance.comment if instance.comment else "Нет"}

🔗 **Подробнее:** [Ссылка на заказ](http://bulka-play.ru/s3cr3t_4dm1n_bulk4_pl4y2_p4th/core/order/{instance.id}/change/)
        """

        # Отправляем сообщение в Telegram
        asyncio.run(send_telegram_message(api_key, user_id, tg_markdown_message))
    except Exception as e:
        print(f"Ошибка отправки сообщения в Telegram: {e}")


@receiver(post_save, sender=Order)
def notify_telegram_on_order_created(sender, instance, created, **kwargs):
    if created:
        print("Order created, waiting for m2m changes...")
        # Мы не отправляем уведомление здесь, а ждем m2m_changed


@receiver(m2m_changed, sender=Order.products.through)
@receiver(m2m_changed, sender=Order.additional_products.through)
@receiver(m2m_changed, sender=Order.arenda.through)
@receiver(m2m_changed, sender=Order.games_for_rent.through)
def notify_telegram_on_order_m2m_changed(sender, instance, action, **kwargs):
    if action == "post_add" and isinstance(instance, Order):
        print("M2M relations changed, sending notification...")
        transaction.on_commit(lambda: send_telegram_notification(instance))
