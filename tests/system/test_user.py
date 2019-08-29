import json

from models.user import UserModel
from tests.base_test import BaseTest


class UserNonLoggedTest(BaseTest):
    def test_register_user(self):
        with self.app() as client:
            with self.app_context():
                # Setup

                # Exercise
                path = '/register'
                headers = {'Content-Type': 'application/json'}
                data = json.dumps({'username': 'test', 'password': '1234'})
                response = client.post(path, headers=headers, data=data)

                # Verify
                expected = {'message': 'User created successfully.'}

                self.assertEqual(201, response.status_code)
                self.assertDictEqual(expected, json.loads(response.data))
                self.assertIsNotNone(UserModel.find_by_username('test'))

    def test_register_duplicate_user(self):
        with self.app() as client:
            with self.app_context():
                # Setup
                UserModel('test', '1234').save_to_db()

                # Exercise
                path = '/register'
                headers = {'Content-Type': 'application/json'}
                data = json.dumps({'username': 'test', 'password': '1234'})
                response = client.post(path, headers=headers, data=data)

                # Verify
                expected = {'message': 'A user with that username already exists.'}

                self.assertEqual(400, response.status_code)
                self.assertDictEqual(expected, json.loads(response.data))


class UserLoggedTest(BaseTest):
    pass
