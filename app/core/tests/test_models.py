from django.test import TestCase
from django.contrib.auth import get_user_model
from ..models import Role


class ModelTests(TestCase):

    def test_create_user(self):
        """Test creating a new user"""
        email = 'test@test.com'
        password = 'testPass'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertEqual(user.role, Role.PLAYER)
        self.assertTrue(user.check_password(password))
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)

    def test_new_user_invalid_email(self):
        """Test creating a new user without an email raises an error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, '123')

    def test_create_new_super_user(self):
        """Test creating a new superuser"""
        user = get_user_model().objects.create_superuser(
            'test@test.con', 'test123'
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
        self.assertEqual(user.role, Role.ADMIN)
