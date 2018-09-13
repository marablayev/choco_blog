from django.urls import path, include

from rest_framework import routers
from rest_framework_jwt import views as jwt_views

from .views import AuthViewSet

router = routers.DefaultRouter()
router.register(r'', AuthViewSet)

urlpatterns = [
    path(r'login/', jwt_views.obtain_jwt_token, name="login"),
    path(r'', include(router.urls)),
]
