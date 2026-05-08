from celery import shared_task
from django.core.mail import send_mail

from config import settings
from lms.models import Course


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
