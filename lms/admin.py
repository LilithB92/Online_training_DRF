from django.contrib import admin

from lms.models import Course
from lms.models import Lesson


# Register your models here.
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    """
    Администрирование модели Курсов(Course).
    Супер позволяет управлять курсами.
    """

    list_display = ("pk", "title", "preview", "description")


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    """
    Администрирование модели Уроков(Lesson).
    Супер позволяет управлять уроками.
    """

    list_display = ("pk", "title", "preview", "description", "video_url", "course")
