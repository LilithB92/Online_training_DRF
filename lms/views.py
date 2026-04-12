from rest_framework import viewsets

from lms.models import Course
from lms.serializers import CourseSerializer


class CourseViewSet(viewsets.ViewSet):
    """CRUD для курса"""
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
