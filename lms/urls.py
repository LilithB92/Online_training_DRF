from django.urls import path
from rest_framework.routers import DefaultRouter

from lms.apps import LmsConfig
from lms.views import CourseViewSet
from lms.views import LessonCreateApiView
from lms.views import LessonDestroyAPIView
from lms.views import LessonListApiView
from lms.views import LessonRetrieveAPIView
from lms.views import LessonUpdateAPIView

app_name = LmsConfig.name

router = DefaultRouter()
router.register(r"courses", CourseViewSet, basename="courses")

urlpatterns = [
    path("lessons/", LessonListApiView.as_view()),
    path("lessons/<int:pk>/", LessonRetrieveAPIView.as_view()),
    path("lessons/create/", LessonCreateApiView.as_view()),
    path("lessons/<int:pk>/update/", LessonUpdateAPIView.as_view()),
    path("lessons/<int:pk>/delete", LessonDestroyAPIView.as_view()),
]

urlpatterns += router.urls
