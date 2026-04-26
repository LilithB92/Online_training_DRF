from rest_framework.serializers import ModelSerializer

from users.models import Payment
from users.models import User


class PaymentSerializer(ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"
        read_only_fields = ["payment_date", "user"]


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email", "phone_number", "avatar", "country", "password")
