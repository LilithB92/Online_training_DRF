from django.urls import path
from rest_framework.routers import DefaultRouter

from lms.apps import LmsConfig
from lms.views import CourseViewSet, LessonListApiView, LessonUpdateAPIView, LessonCreateApiView, LessonDestroyAPIView, LessonRetrieveAPIView

app_name = LmsConfig.name

router = DefaultRouter()
router.register(r"courses", CourseViewSet, basename="courses"),

urlpatterns = [
    path("lessons/", LessonListApiView.as_view()),
    path("lessons/<int:pk>/", LessonRetrieveAPIView.as_view()),
    path("lessons/create/", LessonCreateApiView.as_view()),
    path("lessons/<int:pk>/update/", LessonUpdateAPIView.as_view()),
    path("lessons/<int:pk>/delete", LessonDestroyAPIView.as_view()),
              ] + router.urls
