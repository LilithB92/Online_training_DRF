import os

from django.core.management.base import BaseCommand

from users.models import User


class Command(BaseCommand):
    help = "Создать супер юзера"

    def add_arguments(self, parser):
        parser.add_argument("--email", type=str, help="Email суперпользователя")
        parser.add_argument("--password", type=str, help="Пароль суперпользователя")

    def handle(self, *args, **options):
        email = options["email"] or os.getenv("SUPERUSER_EMAIL", "admin@example.com")
        password = options["password"] or os.getenv("SUPERUSER_PASSWORD", "admin12345")
        user, created = User.objects.get_or_create(
            email=email,
            defaults={"is_active": True, "is_staff": True, "is_superuser": True},
        )
        if created:
            user.set_password(password)
            user.save()
            self.stdout.write(self.style.SUCCESS(f"Successfully created superuser: {user.email}"))
        else:
            self.stdout.write(self.style.WARNING(f"Superuser already exists: {user.email}"))
