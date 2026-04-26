from rest_framework import viewsets
from rest_framework.generics import CreateAPIView
from rest_framework.generics import DestroyAPIView
from rest_framework.generics import ListAPIView
from rest_framework.generics import RetrieveAPIView
from rest_framework.generics import UpdateAPIView
from rest_framework.permissions import IsAuthenticated

from lms.models import Course
from lms.models import Lesson
from lms.serializers import CourseDetailSerializer
from lms.serializers import CourseSerializer
from lms.serializers import LessonSerializer
from users.permissions import IsModerator


class CourseViewSet(viewsets.ModelViewSet):
    """CRUD для курса"""

    queryset = Course.objects.all()

    def get_serializer_class(self):
        """Для извлечения или чтения данных используется `CourseDetailSerializer`, a
        в остальном случаи: `CourseSerializer`"""
        if self.action == "retrieve":
            return CourseDetailSerializer
        return CourseSerializer

    def get_permissions(self):
        """Задает прав для каждого эндпойнта"""
        if self.action == "create":
            self.permission_classes = (IsAuthenticated, ~IsModerator)
        elif self.action in ["list", "retrieve", "update", "partial_update"]:
            self.permission_classes = (IsAuthenticated, IsModerator)
        elif self.action == "destroy":
            self.permission_classes = (IsAuthenticated, ~IsModerator)
        return super().get_permissions()


class LessonCreateApiView(CreateAPIView):
    """Создание одной сущности урока"""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, ~IsModerator)


class LessonListApiView(ListAPIView):
    """Получение списка уроков"""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonRetrieveAPIView(RetrieveAPIView):
    """Получение одной сущности урока"""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonUpdateAPIView(UpdateAPIView):
    """Изменение одной сущности урока"""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonDestroyAPIView(DestroyAPIView):
    """Удаление одной сущности урока"""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, ~IsModerator)
