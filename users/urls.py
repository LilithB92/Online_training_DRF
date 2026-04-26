from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView

from .apps import UsersConfig
from .views import PaymentViewSet

app_name = UsersConfig.name

router = DefaultRouter()
router.register(r"payment", PaymentViewSet)

urlpatterns = [
    path("login/", TokenObtainPairView.as_view(), name="login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
urlpatterns += router.urls
