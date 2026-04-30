from django.conf import settings
from django.db import models


class Course(models.Model):
    """
    Stores a single course entry, related to :model:`lms.Lesson` and :model:`users.User`
    """

    title = models.CharField(max_length=200, verbose_name="Название курса")
    # Поле для картинки, сохраняется в MEDIA_ROOT/courses/
    preview = models.ImageField(upload_to="courses/", verbose_name="Превью", blank=True, null=True)
    course_url = models.URLField(verbose_name="Ссылка на курс", blank=True, null=True)
    description = models.TextField(verbose_name="Описание курса", blank=True, null=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Владелец",
        related_name="courses",
    )

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"

    def __str__(self):
        return self.title


class Lesson(models.Model):
    """
    Stores a single lesson entry, related to :model:`lms.Course` and :model:`users.User`.
    """

    title = models.CharField(max_length=200, verbose_name="Название урока")
    description = models.TextField(verbose_name="Описание урока", blank=True, null=True)
    preview = models.ImageField(upload_to="lessons/previews/", verbose_name="Превью", blank=True, null=True)
    video_url = models.URLField(verbose_name="Ссылка на видео", blank=True, null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="Курс", related_name="lessons")
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Владелец",
        related_name="lessons",
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
