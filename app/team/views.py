from core.models import Team, Role
from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, BasePermission

from . import serializers


class IsAuthorised(BasePermission):
    """Allows access only to authenticated users."""

    def has_permission(self, request, view):
        return bool(request.user and request.user.role != Role.PLAYER)


class TeamViewSet(viewsets.ModelViewSet):
    """Manage Teams in the database"""
    serializer_class = serializers.TeamSerializer
    queryset = Team.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsAuthorised)

    def get_queryset(self):
        if self.request.user.role == Role.COACH:
            """Return objects for the current authenticated user only"""
            return self.queryset.filter(coach=self.request.user.email)
        return self.queryset

    def get_serializer_class(self):
        """Return appropriate serializer class"""
        if self.action == 'retrieve':
            return serializers.TeamDetailSerializer
        return self.serializer_class

    def perform_create(self, serializer):
        print('self.request.user', self.request.user.role)
        serializer.save()


class PlayerViewSet(mixins.ListModelMixin, mixins.CreateModelMixin):
    """Creates a new Player in the database"""
    serializer_class = serializers.PlayerSerializer
