from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from core.models import Role, Team, Player
from team.serializers import TeamSerializer

TEAM_URL = reverse('team:team-list')

def team_detail_url(team_id):
    return reverse('team:team-detail', args=[team_id])


class PublicRecipeApiTest(TestCase):
    """Test without user login"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that the endpoint is not publicly accessible"""
        res = self.client.get(TEAM_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


def create_user(email, password='testPass', role=Role.PLAYER):
    """Create and return a User"""
    return get_user_model().objects.create_user(email=email, password=password, role=role)


def create_team(name, coach):
    """Create and return a Team"""
    return Team.objects.create(name=name, coach=coach)

def create_player(name, height, team):
    """Create and return a Player"""
    return Player.objects.create(name=name, height=height, team=team)


class PrivateRecipeApiTest(TestCase):
    def setUp(self):
        self.user_player = create_user(email='player1@test.com')
        self.user_coach = create_user(email='coach1@test.com', role=Role.COACH)
        self.user_admin = create_user(email='admin1@test.com', role=Role.ADMIN)
        self.client = APIClient()

    def test_retrieve_team_by_player_invalid(self):
        """Test that a player can not access the team endpoint"""
        self.client.force_authenticate(self.user_player)
        res = self.client.get(TEAM_URL)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_teams_by_coach(self):
        """Test that coach can access only the team assigned to him/her"""



        team1 = create_team('Test T1', 'coach1@test.com')
        team2 = create_team('Test T2', 'coach2@test.com')

        player1 = create_player('P1', 45, team1)
        player2 = create_player('P1', 45, team1)

        team1.players.add(player1)
        team1.players.add(player2)

        self.client.force_authenticate(self.user_coach)
        res = self.client.get(TEAM_URL)

        teams = Team.objects.filter(coach='coach1@test.com')
        serializer = TeamSerializer(teams, many=True)

        print('res.data', res.data)
        print('res.data', res.data[0]['players'])
        print('serialized.data', serializer.data)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data, serializer.data)

    def test_retrieve_teams_by_admin(self):
        """Test that admin can access all teams data"""
        create_team('Test T1', 'coach1@test.com')
        create_team('Test T2', 'coach2@test.com')

        self.client.force_authenticate(self.user_admin)
        res = self.client.get(TEAM_URL)

        teams = Team.objects.all();
        serializer = TeamSerializer(teams, many=True)

        # print('res.data', res.data)
        # print('serialized.data', serializer.data)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)
        self.assertEqual(res.data, serializer.data)
