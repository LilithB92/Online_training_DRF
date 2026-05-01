from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from lms.models import Course
from lms.models import CourseSubscription
from lms.models import Lesson
from users.models import User


class LessonAPITestCase(APITestCase):
    def setUp(self):
        """Подготовка данных перед каждым тестом"""
        self.user = User.objects.create(email="test@mail.ru")
        self.course = Course.objects.create(title="python", owner=self.user)
        self.lesson = Lesson.objects.create(title="python types", course=self.course, owner=self.user)
        self.client.force_authenticate(user=self.user)

    def test_lesson_list(self):
        """Тестирование GET-запроса к API(просмотр սպիսօկ урокօվ)"""
        self.url = reverse(viewname="lms:lesson_list")
        response = self.client.get(self.url)
        data = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.lesson.pk,
                    "title": self.lesson.title,
                    "description": None,
                    "preview": None,
                    "video_url": None,
                    "course": self.course.pk,
                    "owner": self.user.id,
                }
            ],
        }
        result = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)

    def test_lesson_details(self):
        """Тестирование GET-запроса к API(просмотр каждого урока)"""
        self.url = reverse(viewname="lms:lesson_detail", args=(self.lesson.pk,))
        response = self.client.get(self.url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("title"), self.lesson.title)

    def test_lesson_create(self):
        """Тестирование POST-запроса к API(создание урока)"""

        self.url = reverse(viewname="lms:lesson_create")
        lesson_dict = {
            "title": "python types",
            "course": self.course.id,
            "video_url": "https://www.youtube.com/watch?v=Ft3PA3eCtcM",
        }
        response = self.client.post(self.url, lesson_dict)
        if response.status_code != 201:
            print(response.data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()["title"], "python types")
        self.assertEqual(Lesson.objects.all().count(), 2)

    def test_lesson_update(self):
        """Тестирование Patch-запроса к API(обновление урока)"""
        self.url = reverse(viewname="lms:lesson_update", args=(self.lesson.pk,))
        lesson_dict = {"title": "python introduction", "video_url": "https://www.youtube.com/watch?v=Ft3PA3eCtcM"}
        response = self.client.patch(self.url, lesson_dict)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("title"), "python introduction")

    def test_lesson_delete(self):
        """Тестирование DELETE-запроса к API(удаление урока)"""
        self.url = reverse(viewname="lms:lesson_delete", args=(self.lesson.pk,))
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.all().count(), 0)


class SubscriptionAPITestCase(APITestCase):
    """Тестирование функционала подписок на курсы."""

    def setUp(self):
        """Подготовка данных для тестов."""
        self.user = User.objects.create(email="test@mail.ru")
        self.course = Course.objects.create(title="python", owner=self.user)
        self.url = reverse(viewname="lms:course_subscribe")
        # Авторизуем пользователя
        self.client.force_authenticate(user=self.user)

    def test_subscribe_to_course(self):
        """Тестирование добавления подписки."""
        data = {"course_id": self.course.id}
        response = self.client.post(self.url, data=data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["message"], "подписка добавлена")
        self.assertTrue(CourseSubscription.objects.filter(user=self.user, course=self.course).exists())

    def test_unsubscribe_from_course(self):
        """Тестирование удаления подписки (toggle)."""

        # Сначала создаем подписку
        CourseSubscription.objects.create(user=self.user, course=self.course)
        data = {"course_id": self.course.pk}
        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["message"], "подписка удалена")
        self.assertFalse(CourseSubscription.objects.filter(user=self.user, course=self.course).exists())

    def test_is_subscribed_field(self):
        """Тестирование наличия признака подписки в данных курса."""
        CourseSubscription.objects.create(user=self.user, course=self.course)
        course_detail_url = reverse("lms:courses-detail", args=(self.course.pk,))
        response = self.client.get(course_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["is_subscribed"], True)
