from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import GameViewSet

app_name = 'game'

router = DefaultRouter()
router.register('', GameViewSet)

urlpatterns = [
    path('', include(router.urls))
]
