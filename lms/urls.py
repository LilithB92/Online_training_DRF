from django.urls import path
from rest_framework.routers import DefaultRouter

from lms.apps import LmsConfig
from lms.views import CourseViewSet
from lms.views import LessonCreateApiView
from lms.views import LessonDestroyAPIView
from lms.views import LessonListApiView
from lms.views import LessonRetrieveAPIView
from lms.views import LessonUpdateAPIView
from users.views import SubscriptionAPIView

app_name = LmsConfig.name

router = DefaultRouter()
router.register(r"courses", CourseViewSet, basename="courses")

urlpatterns = [
    path("lessons/", LessonListApiView.as_view(), name="lesson_list"),
    path("lessons/<int:pk>/", LessonRetrieveAPIView.as_view(), name="lesson_detail"),
    path("lessons/create/", LessonCreateApiView.as_view(), name="lesson_create"),
    path("lessons/<int:pk>/update/", LessonUpdateAPIView.as_view(), name="lesson_update"),
    path("lessons/<int:pk>/delete/", LessonDestroyAPIView.as_view(), name="lesson_delete"),
    path('course/subscribe/', SubscriptionAPIView.as_view(), name='course-subscribe')
]

urlpatterns += router.urls
