from django.core.management.base import BaseCommand

from lms.models import Course
from users.models import Payment
from users.models import User


class Command(BaseCommand):
    help = "Заполнение таблицы Payment начальными данными"

    def handle(self, *args, **kwargs):
        user, _ = User.objects.get_or_create(email="john@example.com", defaults={"password": "johnpassword"})
        course, _ = Course.objects.get_or_create(title="python", description="good course")
        course1, _ = Course.objects.get_or_create(title="php", description="good course")

        payments = [
            {"user": user, "course": course, "amount": 57000, "payment_method": "cash"},
            {"user": user, "course": course1, "amount": 25000, "payment_method": "cash"},
            {"user": user, "course": course, "amount": 30000, "payment_method": "cash"},
            {"user": user, "course": course1, "amount": 12000, "payment_method": "transfer"},
            {"user": user, "course": course, "amount": 83000, "payment_method": "transfer"},
        ]

        for payment_data in payments:
            payment, created = Payment.objects.get_or_create(**payment_data)
            if created:
                self.stdout.write(self.style.SUCCESS(f"Successfully added payment: {payment}"))
            else:
                self.stdout.write(self.style.WARNING(f"Payment already exists: {payment}"))
