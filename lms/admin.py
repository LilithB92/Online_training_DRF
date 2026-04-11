from django.contrib import admin

from lms.models import Course


# Register your models here.
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("pk", "title", "preview", "description")
