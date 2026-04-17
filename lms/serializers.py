from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from lms.models import Course
from lms.models import Lesson


class CourseSerializer(ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"


class CourseDetailSerializer(ModelSerializer):
    lessons_count = SerializerMethodField()
    lessons_title = SerializerMethodField()

    def get_lessons_count(self, obj):
        return Lesson.objects.filter(course=obj.pk).count()

    def get_lessons_title(self, obj):
        return [lesson.title for lesson in Lesson.objects.filter(course=obj.pk)]

    class Meta:
        model = Course
        fields = ("title", "description", "lessons_count", "lessons_title",)
