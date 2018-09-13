from django.urls import path, include

from rest_framework import routers

from .views import PostViewSet, CategoryViewSet, CommentViewSet, RateViewSet

router = routers.DefaultRouter()
router.register('post', PostViewSet)
router.register('category', CategoryViewSet)
router.register('comment', CommentViewSet)
router.register('rate', RateViewSet)

urlpatterns = [
    path(r'', include(router.urls)),
]
