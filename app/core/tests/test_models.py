from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        """test creating a new user with an email is successful"""
        email = 'test@test.com'
        password = 'testPass'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        print(repr(user))

        self.assertEqual(user.email, email)
        self.assertEqual(user.role, 3)
        self.assertTrue(user.check_password(password))
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)