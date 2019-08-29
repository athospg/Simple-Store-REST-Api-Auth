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

    def test_login_user_wrong_credentials(self):
        with self.app() as client:
            with self.app_context():
                # Setup
                UserModel('test', '1234').save_to_db()

                # Exercise
                path = '/login'
                headers = {'Content-Type': 'application/json'}
                data = json.dumps({'username': 'test', 'password': '4321'})
                response = client.post(path, headers=headers, data=data)

                # Verify
                expected = {'message': 'Invalid credentials'}

                self.assertEqual(401, response.status_code)
                self.assertDictEqual(expected, json.loads(response.data))

    def test_login_user(self):
        with self.app() as client:
            with self.app_context():
                # Setup
                UserModel('test', '1234').save_to_db()

                # Exercise
                path = '/login'
                headers = {'Content-Type': 'application/json'}
                data = json.dumps({'username': 'test', 'password': '1234'})
                auth_response = client.post(path, headers=headers, data=data)

                # Verify
                self.assertIn('access_token', json.loads(auth_response.data).keys())
                self.assertIn('refresh_token', json.loads(auth_response.data).keys())

    def test_get_user(self):
        with self.app() as client:
            with self.app_context():
                # Setup
                UserModel('test', '1234').save_to_db()

                # Exercise
                path = '/user/1'
                response = client.get(path)

                # Verify
                expected = {'description': 'Request does not contain an access token.',
                            'error': 'authorization_required'}

                self.assertEqual(401, response.status_code)
                self.assertDictEqual(expected, json.loads(response.data))


class UserLoggedTest(BaseTest):
    def setUp(self):
        super(UserLoggedTest, self).setUp()
        with self.app() as client:
            with self.app_context():
                UserModel('test', '1234').save_to_db()

                path = '/login'
                headers = {'Content-Type': 'application/json'}
                data = json.dumps({'username': 'test', 'password': '1234'})
                auth_request = client.post(path, headers=headers, data=data)

                access_token = json.loads(auth_request.data)['access_token']
                refresh_token = json.loads(auth_request.data)['refresh_token']

                self.access_token = f'Bearer {access_token}'
                self.refresh_token = f'Bearer {refresh_token}'

    def test_get_user(self):
        with self.app() as client:
            with self.app_context():
                # Setup

                # Exercise
                path = '/user/1'
                headers = {'Authorization': self.access_token}
                response = client.get(path, headers=headers)

                # Verify
                expected = {'id': 1, 'username': 'test'}

                self.assertEqual(200, response.status_code)
                self.assertDictEqual(expected, json.loads(response.data))

    def test_refresh_token(self):
        with self.app() as client:
            with self.app_context():
                # Setup

                # Exercise
                path = '/refresh'
                headers = {'Authorization': self.refresh_token}
                auth_response = client.post(path, headers=headers)

                # Verify
                self.assertIn('access_token', json.loads(auth_response.data).keys())

                access_token = json.loads(auth_response.data)['access_token']

                self.assertNotEqual(self.access_token, access_token)

    def test_delete_user_without_fresh(self):
        with self.app() as client:
            with self.app_context():
                # Setup
                auth_request = client.post(
                    '/refresh',
                    headers={'Authorization': self.refresh_token}
                )
                access_token = json.loads(auth_request.data)['access_token']

                # Exercise
                path = '/user/1'
                headers = {'Authorization': f'Bearer {access_token}'}
                resp = client.delete(path, headers=headers)

                # Verify
                expected = {
                    'description': 'The token is not fresh.',
                    'error': 'fresh_token_required'
                }

                self.assertEqual(401, resp.status_code)
                self.assertDictEqual(expected, json.loads(resp.data))

    def test_delete_user(self):
        with self.app() as client:
            with self.app_context():
                # Setup

                # Exercise
                path = '/user/1'
                headers = {'Authorization': self.access_token}
                resp = client.delete(path, headers=headers)

                # Verify
                expected = {'message': 'User deleted'}

                self.assertEqual(200, resp.status_code)
                self.assertDictEqual(expected, json.loads(resp.data))
