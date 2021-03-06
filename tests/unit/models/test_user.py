from unittest import TestCase

from models.user import UserModel


class UserTest(TestCase):
    def test_create_user(self):
        # Setup

        # Exercise
        user = UserModel('test', 'abcd')

        # Verify
        self.assertEqual('test', user.username)
        self.assertEqual('abcd', user.password)

    def test_user_json(self):
        # Setup

        # Exercise
        item = UserModel('test', 'abcd')

        # Verify
        expected = {'id': None, 'username': 'test'}
        self.assertEqual(expected, item.json())
