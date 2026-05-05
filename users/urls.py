from django.urls import path
from rest_framework.permissions import AllowAny
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView

from .apps import UsersConfig
from .views import PaymentCourseCreateApiView
from .views import PaymentStatusView
from .views import PaymentViewSet
from .views import UserCreateAPIView
from .views import UserDestroyAPIView
from .views import UserListApiView
from .views import UserRetrieveAPIView
from .views import UserUpdateAPIView

app_name = UsersConfig.name

router = DefaultRouter()
router.register(r"payment", PaymentViewSet)

urlpatterns = [
    path("register/", UserCreateAPIView.as_view(), name="register"),
    path("login/", TokenObtainPairView.as_view(permission_classes=(AllowAny,)), name="login"),
    path("token/refresh/", TokenRefreshView.as_view(permission_classes=(AllowAny,)), name="token_refresh"),
    path("list/", UserListApiView.as_view(), name="user_list"),
    path("detail/<int:pk>/", UserRetrieveAPIView.as_view(), name="user_detail"),
    path("update/<int:pk>/", UserUpdateAPIView.as_view(), name="update"),
    path("delete/<int:pk>/", UserDestroyAPIView.as_view(), name="delete"),
    path("course_payment/", PaymentCourseCreateApiView.as_view(), name="course_payment_create"),
    path("payment/status/<int:pk>/", PaymentStatusView.as_view(), name="payment_status"),
]
urlpatterns += router.urls
