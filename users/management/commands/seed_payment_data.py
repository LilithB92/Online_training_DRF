from django.core.management.base import BaseCommand

from lms.models import Course
from users.models import Payment
from users.models import User


class Command(BaseCommand):
    help = "Заполнение таблицы Payment начальными данными"

    def handle(self, *args, **kwargs):
        user, _ = User.objects.get_or_create(username="john", password="johnpassword", email="john@example.com")
        course, _ = Course.objects.get_or_create(title="python", description="good course")

        payments = [
            {"user": user, "course": course, "amount": 57000.50, "payment_method": "cash"},
            {"user": user, "course": course, "amount": 25000.50, "payment_method": "cash"},
            {"user": user, "course": course, "amount": 30000.50, "payment_method": "cash"},
        ]

        for payment_data in payments:
            payment, created = Payment.objects.get_or_create(**payment_data)
            if created:
                self.stdout.write(self.style.SUCCESS(f"Successfully added payment: {payment.__str__()}"))
            else:
                self.stdout.write(self.style.WARNING(f"Payment already exists: {payment.__str__()}"))
