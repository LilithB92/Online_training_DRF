from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework import viewsets
from rest_framework.generics import CreateAPIView
from rest_framework.generics import DestroyAPIView
from rest_framework.generics import ListAPIView
from rest_framework.generics import RetrieveAPIView
from rest_framework.generics import UpdateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated

from users.models import Payment
from users.models import User
from users.permissions import IsOwner
from users.permissions import IsUserOwner
from users.serializers import PaymentSerializer
from users.serializers import UserSerializer


class PaymentViewSet(viewsets.ModelViewSet):
    """Получение CRUD Платежи"""

    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ["course", "lesson", "payment_method"]
    ordering_fields = ["payment_date"]


class UserCreateAPIView(CreateAPIView):
    """Регистрация пользователя"""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class UserListApiView(ListAPIView):
    """Получение списка уроков"""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = IsAuthenticated


class UserRetrieveAPIView(RetrieveAPIView):
    """Получение одной сущности урока"""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = IsAuthenticated


class UserUpdateAPIView(UpdateAPIView):
    """Изменение одной сущности пользователя"""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, IsOwner)


class UserDestroyAPIView(DestroyAPIView):
    """Удаление одной сущности пользователя"""

    queryset = User.objects.all()
    permission_classes = (IsAuthenticated, IsUserOwner)
