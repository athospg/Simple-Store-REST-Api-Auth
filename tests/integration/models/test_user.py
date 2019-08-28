from models.user import UserModel
from tests.base_test import BaseTest


class UserTest(BaseTest):
    def test_crud(self):
        """
        CRUD: Create, Read, Update and Delete.
        These are the four major and basic functions of persistent storage.
        """
        with self.app_context():
            # Setup
            user = UserModel('test', 'abcd')

            # Exercise

            # Verify
            self.assertIsNone(UserModel.find_by_username('test'))
            self.assertIsNone(UserModel.find_by_id(1))

            # Exercise
            user.save_to_db()

            # Verify
            self.assertIsNotNone(UserModel.find_by_username('test'))
            self.assertIsNotNone(UserModel.find_by_id(1))

            # Exercise
            user.delete_from_db()

            # Verify
            self.assertIsNone(UserModel.find_by_username('test'))
            self.assertIsNone(UserModel.find_by_id(1))
