from django.contrib import admin

from users.models import Payment
from users.models import User


# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """
    Администрирование модели Пользователь(User).
    Супер позволяет управлять пользователями и их активностью.
    """

    list_display = ("id", "email", "phone_number", "avatar", "country")


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    """
    Администрирование модели Оплат(Payment).
    Супер пользователь следит за оплатами.
    """

    list_display = (
        "user",
        "payment_date",
        "course",
        "lesson",
        "amount",
    )

    # Removes the ability to add new objects
    def has_add_permission(self, request):
        return False

    # Removes the ability to delete objects
    def has_delete_permission(self, request, obj=None):
        return False

    # Removes the ability to change objects
    def has_change_permission(self, request, obj=None):
        return False
