from rest_framework import status
from rest_framework import viewsets
from rest_framework.generics import CreateAPIView
from rest_framework.generics import DestroyAPIView
from rest_framework.generics import ListAPIView
from rest_framework.generics import RetrieveAPIView
from rest_framework.generics import UpdateAPIView
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from lms.models import Course
from lms.models import CourseSubscription
from lms.models import Lesson
from lms.paginators import LessonCoursePagination
from lms.serializers import CourseDetailSerializer
from lms.serializers import CourseSerializer
from lms.serializers import LessonSerializer
from lms.services import get_course_subscribed_user
from lms.tasks import send_course_update_email
from users.permissions import IsModerator
from users.permissions import IsOwner


class CourseViewSet(viewsets.ModelViewSet):
    """CRUD для курса"""

    queryset = Course.objects.all().order_by("pk")
    pagination_class = LessonCoursePagination

    def get_serializer_class(self):
        """Для извлечения или чтения данных используется `CourseDetailSerializer`, a
        в остальном случаи: `CourseSerializer`"""
        if self.action == "retrieve":
            return CourseDetailSerializer
        return CourseSerializer

    def perform_create(self, serializer):
        """При создании курса поле для владельца сущности заполняется аутентифицированным пользователем."""

        course = serializer.save()
        course.owner = self.request.user
        course.save()

    def perform_update(self, serializer):
        """ Обновляет курс и отправляет почту об обновление пользователям подписании на этот курс"""
        course_id = self.kwargs.get("pk")
        emails = get_course_subscribed_user(course_id)
        serializer.save()
        send_course_update_email.delay(course_id=course_id, subscribed_users_emails=emails)

    def get_permissions(self):
        """Задает прав для каждого эндпойнта"""
        if self.action == "create":
            self.permission_classes = (IsAuthenticated, ~IsModerator)
        elif self.action in ["list", "retrieve", "update", "partial_update"]:
            self.permission_classes = (IsAuthenticated, IsModerator | IsOwner)
        elif self.action == "destroy":
            self.permission_classes = (IsAuthenticated, IsOwner | ~IsModerator)
        return super().get_permissions()


class LessonCreateApiView(CreateAPIView):
    """Создание одной сущности урока"""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, ~IsModerator)

    def perform_create(self, serializer):
        """При создании урока поле для владельца сущности заполняется аутентифицированным пользователем."""

        lesson = serializer.save()
        lesson.owner = self.request.user
        lesson.save()


class LessonListApiView(ListAPIView):
    """Получение списка уроков"""

    queryset = Lesson.objects.all().order_by("pk")
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, IsOwner | IsModerator)
    pagination_class = LessonCoursePagination


class LessonRetrieveAPIView(RetrieveAPIView):
    """Получение одной сущности урока"""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, IsOwner | IsModerator)


class LessonUpdateAPIView(UpdateAPIView):
    """Изменение одной сущности урока"""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, IsOwner | IsModerator)


class LessonDestroyAPIView(DestroyAPIView):
    """Удаление одной сущности урока"""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, ~IsModerator | IsOwner)


class SubscriptionAPIView(APIView):
    """API View для управления подпиской пользователя на курс.

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
        course_id = self.request.data.get("course_id")
        if not course_id:
            return Response({"error": "course_id is required"}, status=status.HTTP_400_BAD_REQUEST)
        course_item = get_object_or_404(Course, id=course_id)
        subs_item = CourseSubscription.objects.filter(user=user, course=course_item)
        if subs_item.exists():
            subs_item.delete()
            message = "подписка удалена"
        else:
            CourseSubscription.objects.create(user=user, course=course_item)
            message = "подписка добавлена"
        return Response({"message": message}, status=status.HTTP_200_OK)
