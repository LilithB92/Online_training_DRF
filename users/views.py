from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework import filters, status
from rest_framework import viewsets
from rest_framework.generics import CreateAPIView, get_object_or_404
from rest_framework.generics import DestroyAPIView
from rest_framework.generics import ListAPIView
from rest_framework.generics import RetrieveAPIView
from rest_framework.generics import UpdateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from lms.models import CourseSubscription, Course
from users.models import Payment
from users.models import User
from users.permissions import IsUserOwner
from users.serializers import PaymentSerializer
from users.serializers import UserGeneralInformationSerializer
from users.serializers import UserSerializer
from users.serializers import UserUpdateSerializer


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


class SubscriptionAPIView(APIView):
    """ API View для управления подпиской пользователя на курс.

    Работает в режиме 'toggle' (переключатель): если подписки нет — создает,
    если есть — удаляет.
    """
    permission_classes = [IsAuthenticated]

    def post(self, *args, **kwargs):
        """
      Обрабатывает POST-запрос на изменение статуса подписки.
      Ожидает в body:
      {
          "course": <int:id_курса>
      }
      """
        user = self.request.user
        course_id = self.request.data.get('course_id')
        if not course_id:
            return Response(
                {"error": "course_id is required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        course_item = get_object_or_404(Course, id=course_id)
        subs_item = CourseSubscription.objects.filter(user=user, course=course_item)
        if subs_item.exists():
            subs_item.delete()
            message = 'подписка удалена'
        else:
            CourseSubscription.objects.create(user=user, course=course_item)
            message = 'подписка добавлена'
        return Response({"message": message}, status=status.HTTP_200_OK)
