from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class User(AbstractUser):
    email = models.EmailField(unique=True, verbose_name="Почта", help_text="Введите Вашу почту")
    phone_number = models.CharField(
        max_length=30, blank=True, null=True, verbose_name="Телефон", help_text="Введите Ваш номер телефона"
    )
    avatar = models.ImageField(upload_to="users/avatars/", blank=True, null=True, verbose_name="Аватарка")
    country = models.CharField(
        max_length=60, blank=True, null=True, verbose_name="Страна", help_text="Введите Ваша страна"
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [
        "username",
    ]

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = ("Пользователь",)
        verbose_name_plural = "Пользователи"
