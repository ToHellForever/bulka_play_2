from django import template

register = template.Library()

@register.filter
def format_price(value):
    try:
        # Преобразуем значение в число с плавающей точкой
        price = float(value)
        # Форматируем число с разделителями тысяч
        return f"{price:,.0f}".replace(",", " ")
    except (ValueError, TypeError):
        return value
#  poetry run python manage.py runserver