from rest_framework.routers import DefaultRouter

from .apps import UsersConfig
from .views import PaymentViewSet

app_name = UsersConfig.name

router = DefaultRouter()
router.register(r"payment", PaymentViewSet)

urlpatterns = []
urlpatterns += router.urls
