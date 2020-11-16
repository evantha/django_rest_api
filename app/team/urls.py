from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import TeamViewSet

app_name = 'team'

router = DefaultRouter()
router.register('', TeamViewSet)

urlpatterns = [
    path('', include(router.urls))
]
