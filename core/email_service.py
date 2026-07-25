from django.core.mail import send_mail
from django.conf import settings


def send_email_notification(subject, message):
    """Отправка email уведомления"""
    try:
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [settings.EMAIL_RECIPIENT]
        
        send_mail(
            subject=subject,
            message=message,
            from_email=from_email,
            recipient_list=recipient_list,
            fail_silently=False,
        )
        print(f'Email "{subject}" отправлен на {recipient_list}')
        return True
    except Exception as e:
        print(f"Ошибка отправки email: {e}")
        return False
