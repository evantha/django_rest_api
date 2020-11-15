from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


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
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that supports using email instead of username"""

    ADMIN = 1
    COACH = 2
    PLAYER = 3

    ROLE_CHOICES = (
        (ADMIN, 'Admin'),
        (COACH, 'COACH'),
        (PLAYER, 'PLAYER')
    )

    def __str__(self):
        return 'username: ' + str(self.email) + ', name: ' + str(self.name) + ', role:' + str(self.role)

    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, default=3)

    objects = UserManager()
    USERNAME_FIELD = 'email'
