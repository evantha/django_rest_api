from core.models import Team, Player
from rest_framework import serializers


class PlayerSerializer(serializers.ModelSerializer):
    """"Serializer for Player objects"""

    class Meta:
        model = Player
        fields = ['id', 'name', 'height']
        read_only_fields = ['id', ]


class TeamSerializer(serializers.ModelSerializer):
    """"Serializer for Team objects"""

    players = serializers.PrimaryKeyRelatedField(many=True, queryset=Player.objects.all())

    # def create(self, validated_data):
    #     """
    #     Create function for recipes, a restaurant and a list of ingredients is associated. The restaurantId
    #     is taken from the corresponding path parameter and the ingredients can be added optionally in the post body.
    #     """
    #     players_data = validated_data.pop("players")
    #
    #     team = Team.objects.get(pk=validated_data["team_id"])
    #     validated_data["team"] = team
    #     print('validated_data', validated_data)
    #     player = Player.objects.create(**validated_data)
    #
    #     return player

    class Meta:
        model = Team
        fields = ['id', 'name', 'coach', 'players']
        read_only_fields = ['id', ]


class TeamDetailSerializer(TeamSerializer):
    """"Serializer for Team details objects"""
    players = PlayerSerializer
