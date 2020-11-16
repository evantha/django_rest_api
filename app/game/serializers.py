from core.models import Game, Team, Player
from rest_framework import serializers


class GameSerializer(serializers.ModelSerializer):
    # winner = serializers.PrimaryKeyRelatedField()
    teams = serializers.PrimaryKeyRelatedField(many=True, queryset=Team.objects.all())
    players = serializers.PrimaryKeyRelatedField(many=True, queryset=Player.objects.all())

    class Meta:
        model = Game
        fields = ['id', 'duration', 'winner', 'teams', 'players']
        read_only_fields = ['id', ]
