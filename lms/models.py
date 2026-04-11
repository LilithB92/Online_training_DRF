from django.db import models


class Course(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название курса")
    # Поле для картинки, сохраняется в MEDIA_ROOT/courses/
    preview = models.ImageField(upload_to="courses/", verbose_name="Превью", blank=True, null=True)
    description = models.TextField(verbose_name="Описание курса")

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"

    def __str__(self):
        return self.title
