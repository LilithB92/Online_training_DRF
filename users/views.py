from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework import status
from rest_framework import viewsets
from rest_framework.generics import CreateAPIView
from rest_framework.generics import DestroyAPIView
from rest_framework.generics import ListAPIView
from rest_framework.generics import RetrieveAPIView
from rest_framework.generics import UpdateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from users.models import Payment
from users.models import User
from users.permissions import IsUserOwner
from users.serializers import PaymentSerializer
from users.serializers import UserGeneralInformationSerializer
from users.serializers import UserSerializer
from users.serializers import UserUpdateSerializer
from users.services import convert_rub_to_usd
from users.services import create_stipe_session
from users.services import create_stripe_price
from users.services import create_stripe_product
from users.services import get_session_status


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
    """Получение списка пользователей"""

    queryset = User.objects.all()
    serializer_class = UserGeneralInformationSerializer
    permission_classes = (IsAuthenticated,)


class UserRetrieveAPIView(RetrieveAPIView):
    """Получение одной сущности пользователя"""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        """просмотра чужого профиля должна быть доступна только общая информация, а в собственном вся"""
        if self.request.user.id == self.kwargs.get("pk"):
            return UserSerializer
        return UserGeneralInformationSerializer


class UserUpdateAPIView(UpdateAPIView):
    """Изменение одной сущности пользователя"""

    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer
    permission_classes = (IsAuthenticated, IsUserOwner)

    def perform_update(self, serializer):
        """Метод serializer.save() вызывает метод .update(), определенный в UserUpdateSerializer."""
        serializer.save()


class UserDestroyAPIView(DestroyAPIView):
    """Удаление одной сущности пользователя"""

    queryset = User.objects.all()
    permission_classes = (IsAuthenticated, IsUserOwner)


class PaymentCourseCreateApiView(CreateAPIView):
    """Создание одной сущности платежа"""

    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        """Создает session_id страйпа для оплаты курса"""

        try:
            payment = serializer.save(user=self.request.user)
            course = serializer.validated_data.get("course")
            title = course.title
            amount = int(course.price)
            price = convert_rub_to_usd(amount)
            product = create_stripe_product(name=title)
            stripe_price = create_stripe_price(product=product, price=price)
            session_id, payment_link = create_stipe_session(stripe_price)
            print(session_id)
            payment.session_id = session_id
            payment.payment_link = payment_link
            payment.save()
        except Exception as ex:
            return f"Что то пошел не так с платежом: {ex}"


class PaymentStatusView(RetrieveAPIView):
    """Проверяет session_id статус оплати у страйпа, и если оплачен то статус платежа
    меняет оплачен, если нет вернет HTTP_400_BAD_REQUEST"""

    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()

    def get(self, request, *args, **kwargs):
        payment = self.get_object()
        if payment.session_id:
            # Получаем актуальный статус из Stripe
            stripe_session = get_session_status(payment.session_id)

            # Обновляем статус, если он изменился
            if stripe_session["payment_status"] == "paid":
                payment.status = "paid"
                payment.save()

            return Response(
                {
                    "id": payment.pk,
                    "status": payment.status,
                    "stripe_status": stripe_session["payment_status"],
                    "payment_link": payment.payment_link,
                }
            )
        return Response({"error": "No session found"}, status=status.HTTP_400_BAD_REQUEST)
