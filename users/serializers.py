from rest_framework.serializers import ModelSerializer

from users.models import Payment
from users.models import User


class PaymentSerializer(ModelSerializer):
    """
    Сериализатор для модели «Оплаты».

    Обрабатывает преобразование экземпляров оплаты в формат JSON и выполняет валидацию
    входящие данные для удаления, просмотра, создания или обновления оплаты.
    """

    class Meta:
        model = Payment
        fields = "__all__"
        read_only_fields = ["payment_date", "user"]


class UserSerializer(ModelSerializer):
    """
    Сериализатор для модели «Пользователи».

    Обрабатывает преобразование экземпляров пользователи в формат JSON и выполняет валидацию
    входящие данные регистрации пользователи.
    """

    class Meta:
        model = User
        fields = ("id", "email", "phone_number", "avatar", "country", "password")


class UserNotOwnerSerializer(ModelSerializer):
    """
    Сериализатор для модели «Пользователи», не для владельца.

    Обрабатывает преобразование экземпляров пользователи в формат JSON и выполняет просмотра данных.
    """

    class Meta:
        model = User
        fields = (
            "email",
            "phone_number",
            "avatar",
            "country",
        )
