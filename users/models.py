from django.contrib.auth.models import AbstractUser
from django.db import models

from config import settings
from lms.models import Course
from lms.models import Lesson


# Create your models here.
class User(AbstractUser):
    """
    Stores a single user entry, related to :model:`users.Payment`
    """
    username = None
    email = models.EmailField(unique=True, verbose_name="Почта", help_text="Введите Вашу почту")
    phone_number = models.CharField(
        max_length=30, blank=True, null=True, verbose_name="Телефон", help_text="Введите Ваш номер телефона"
    )
    avatar = models.ImageField(upload_to="users/avatars/", blank=True, null=True, verbose_name="Аватарка")
    country = models.CharField(
        max_length=60, blank=True, null=True, verbose_name="Страна", help_text="Введите Ваша страна"
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Payment(models.Model):
    """
    Stores a single payment entry, related to :model:`users.User`,:model:`lms.Lesson` and :model:`lms.Class`
    """

    PAYMENT_METHOD_CHOICES = [
        ("cash", "Наличные"),
        ("transfer", "Перевод на счет"),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="payments")
    payment_date = models.DateTimeField(auto_now_add=True)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, blank=True, related_name="payments")
    lesson = models.ForeignKey(Lesson, on_delete=models.SET_NULL, null=True, blank=True, related_name="payments")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHOD_CHOICES)

    def __str__(self):
        return f"{self.user} - {self.amount} - {self.payment_date}"

    class Meta:
        verbose_name = ("Платеж",)
        verbose_name_plural = "Платежи"
