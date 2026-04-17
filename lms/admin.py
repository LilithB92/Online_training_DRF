from django.contrib import admin

from lms.models import Course
from lms.models import Lesson


# Register your models here.
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("pk", "title", "preview", "description")


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ("pk", "title", "preview", "description", "video_url", "course")
