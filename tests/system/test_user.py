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


class UserLoggedTest(BaseTest):
    pass
