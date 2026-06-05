from datetime import timedelta

from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone

from config import settings
from lms.models import Course
from users.models import User


@shared_task
def send_course_update_email(course_id, subscribed_users_emails):
    """
    Асинхронная задача для отправки писем подписчикам.
    """
    course = Course.objects.get(pk=course_id)
    subject = f"Обновление курса: {course.title}"
    message = f'Здравствуйте! Курс "{course.title}" был обновлен. Проверьте новые материалы.'

    send_mail(
        subject=subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=subscribed_users_emails,  # Список адресов
        fail_silently=False,
    )


@shared_task
def deactivate_inactive_users():
    """
    Блокирует пользователей, которые не заходили более 30 дней и возвращает количество блокированных пользователей.
    """
    one_month_ago = timezone.now() - timedelta(days=30)
    count_inactive_users = User.objects.filter(
        is_active=True,
        last_login__lt=one_month_ago
    ).update(is_active=False)
    print(f"Deactivated {count_inactive_users} inactive users.")
