from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from lms.models import Course
from lms.models import Lesson
from lms.validators import YoutubeChanelValidator


class CourseSerializer(ModelSerializer):
    """
       Сериалайзер для модели «Курс».

       Обрабатывает преобразование экземпляров курса в формат JSON и выполняет валидацию
       входящие данные для удаления, создания или обновления курсов.
       """
    class Meta:
        model = Course
        fields = "__all__"
        validators = [YoutubeChanelValidator(field='course_url')]


class LessonSerializer(ModelSerializer):
    """
       Сериалайзер для модели «Урок».

       Обрабатывает преобразование экземпляров урока в формат JSON и выполняет валидацию
       входящие данные для удаления, просмотра, создания или обновления курсов.
       """
    class Meta:
        model = Lesson
        fields = "__all__"
        validators = [YoutubeChanelValidator(field='video_url')]


class CourseDetailSerializer(ModelSerializer):
    """
    Сериалайзер для модели «Курс».

    Обрабатывает преобразование экземпляров курса в формат JSON и выполняет
     просмотр курсов.
    """
    lessons_count = SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)

    def get_lessons_count(self, obj):
        """Получает количество уроков в курсе"""
        return Lesson.objects.filter(course=obj.pk).count()

    class Meta:
        model = Course
        fields = (
            "title",
            "description",
            "lessons_count",
            "lessons",
        )
