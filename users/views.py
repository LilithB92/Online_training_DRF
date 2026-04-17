from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

from users.models import Payment
from users.serializers import PaymentSerializer


class PaymentViewSet(viewsets.ModelViewSet):
    """Получение CRUD Платежи"""

    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["course", "lesson", "payment_method"]
