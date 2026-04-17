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

    def get_lessons_count(self, obj):
        return Lesson.objects.filter(course=obj.pk).count()

    class Meta:
        model = Course
        fields = ("title", "description", "lessons_count")
