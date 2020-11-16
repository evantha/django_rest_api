from core.models import Game
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from . import serializers


class GameViewSet(viewsets.ModelViewSet):
    """Manage Games in the database"""
    serializer_class = serializers.GameSerializer
    queryset = Game.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
