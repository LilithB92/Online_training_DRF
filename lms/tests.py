from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from lms.models import Course, Lesson
from users.models import User


class LessonAPITestCase(APITestCase):
    def setUp(self):
        """ Подготовка данных перед каждым тестом"""
        self.user = User.objects.create(email="test@mail.ru")
        self.course = Course.objects.create(title='python', owner=self.user)
        self.lesson = Lesson.objects.create(title ="python types", course=self.course, owner=self.user)
        self.client.force_authenticate(user=self.user)

    def test_lesson_details(self):
        """Тестирование GET-запроса к API(просмотр каждого урока)"""
        self.url = reverse(viewname="lms:lesson_detail", args=(self.lesson.pk,))
        response = self.client.get(self.url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get('title'), self.lesson.title)

    def test_lesson_create(self):
        """ Тестирование POST-запроса к API(создание урока)"""

        self.url = reverse(viewname="lms:lesson_create")
        lesson_dict = {"title":"python types", "course":self.course.id,"video_url":"https://www.youtube.com/watch?v=Ft3PA3eCtcM"}
        response = self.client.post(self.url, lesson_dict)
        if response.status_code != 201:
            print(response.data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()['title'], 'python types')
        self.assertEqual(Lesson.objects.all().count(), 2)