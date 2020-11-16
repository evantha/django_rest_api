from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class Role(models.IntegerChoices):
    ADMIN = 1
    COACH = 2
    PLAYER = 3


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        """Creates and saves a new user"""
        if not email:
            raise ValueError('Email must be present')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """creates a new super user"""
        user = self.create_user(email, password, role=Role.ADMIN)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that supports using email instead of username"""

    def __str__(self):
        return 'username: ' + str(self.email) + ', name: ' + str(self.name) + ', role:' + str(self.role)

    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    role = models.PositiveSmallIntegerField(choices=Role.choices, default=Role.PLAYER)

    objects = UserManager()
    USERNAME_FIELD = 'email'


class Team(models.Model):
    name = models.CharField(max_length=255)
    coach = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Player(models.Model):
    name = models.CharField(max_length=255)
    height = models.PositiveSmallIntegerField(default=0)
    team = models.ForeignKey(Team, related_name='players', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Game(models.Model):
    duration = models.IntegerField()
    winner = models.ForeignKey(Team, related_name='team', on_delete=models.CASCADE)
    # winner = models.CharField(max_length=10)
    teams = models.ManyToManyField('Team')
    players = models.ManyToManyField('Player')


class PlayerScore(models.Model):
    game = models.ForeignKey(Game, related_name='game', on_delete=models.CASCADE)
    player = models.ForeignKey(Player, related_name='player', on_delete=models.CASCADE)
    score = models.PositiveSmallIntegerField()

    class Meta:
        unique_together = ['game', 'player']
