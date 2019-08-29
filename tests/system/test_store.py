import json

from models.item import ItemModel
from models.store import StoreModel
from models.user import UserModel
from tests.base_test import BaseTest


# noinspection DuplicatedCode
class StoreTest(BaseTest):
    def setUp(self):
        super(StoreTest, self).setUp()
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

    def test_create_store(self):
        with self.app() as client:
            with self.app_context():
                # Setup

                # Exercise
                path = '/store/test'
                headers = {'Authorization': self.access_token}
                resp = client.post(path, headers=headers)

                # Verify
                expected = {'id': 1, 'name': 'test', 'items': []}

                self.assertEqual(201, resp.status_code)
                self.assertDictEqual(expected, json.loads(resp.data))
                self.assertIsNotNone(StoreModel.find_by_name('test'))

    def test_create_duplicate_store(self):
        with self.app() as client:
            with self.app_context():
                # Setup
                StoreModel('test').save_to_db()

                # Exercise
                path = '/store/test'
                headers = {'Authorization': self.access_token}
                resp = client.post(path, headers=headers)

                # Verify
                expected = {'message': "A store with name 'test' already exists."}

                self.assertEqual(400, resp.status_code)
                self.assertDictEqual(expected, json.loads(resp.data))

    def test_get_store_not_found(self):
        with self.app() as client:
            with self.app_context():
                # Setup

                # Exercise
                path = '/store/test'
                headers = {'Authorization': self.access_token}
                resp = client.get(path, headers=headers)

                # Verify
                expected = {'message': 'Store not found'}

                self.assertEqual(404, resp.status_code)
                self.assertDictEqual(expected, json.loads(resp.data))

    def test_get_store(self):
        with self.app() as client:
            with self.app_context():
                # Setup
                StoreModel('test').save_to_db()

                # Exercise
                path = '/store/test'
                headers = {'Authorization': self.access_token}
                resp = client.get(path, headers=headers)

                # Verify
                expected = {'id': 1, 'name': 'test', 'items': []}

                self.assertEqual(200, resp.status_code)
                self.assertDictEqual(expected, json.loads(resp.data))

    def test_get_store_with_items(self):
        with self.app() as client:
            with self.app_context():
                # Setup
                StoreModel('Store 1').save_to_db()
                ItemModel('Item A', 19.99, 1).save_to_db()

                # Exercise
                path = '/store/Store 1'
                headers = {'Authorization': self.access_token}
                resp = client.get(path, headers=headers)

                # Verify
                expected = {
                    'id': 1,
                    'name': 'Store 1',
                    'items': [{'id': 1, 'name': 'Item A', 'price': 19.99, 'store_id': 1}]
                }

                self.assertEqual(200, resp.status_code)
                self.assertDictEqual(expected, json.loads(resp.data))

    def test_delete_store_without_fresh(self):
        with self.app() as client:
            with self.app_context():
                # Setup
                path = '/refresh'
                headers = {'Authorization': self.refresh_token}
                auth_request = client.post(path, headers=headers)
                access_token = json.loads(auth_request.data)['access_token']

                StoreModel('test').save_to_db()

                # Exercise
                path = '/store/test'
                headers = {'Authorization': f'Bearer {access_token}'}
                resp = client.delete(path, headers=headers)

                # Verify
                expected = {
                    'description': 'The token is not fresh.',
                    'error': 'fresh_token_required'
                }

                self.assertEqual(401, resp.status_code)
                self.assertDictEqual(expected, json.loads(resp.data))

    def test_delete_store(self):
        with self.app() as client:
            with self.app_context():
                # Setup
                StoreModel('test').save_to_db()

                # Exercise
                path = '/store/test'
                headers = {'Authorization': self.access_token}
                resp = client.delete(path, headers=headers)

                # Verify
                expected = {'message': 'Store deleted'}

                self.assertEqual(200, resp.status_code)
                self.assertDictEqual(expected, json.loads(resp.data))

    def test_get_store_list(self):
        with self.app() as client:
            with self.app_context():
                # Setup
                StoreModel('Store A').save_to_db()
                StoreModel('Store B').save_to_db()

                # Exercise
                path = '/stores'
                headers = {'Authorization': self.access_token}
                resp = client.get(path, headers=headers)

                # Verify
                expected = {'stores': [
                    {'id': 1, 'name': 'Store A', 'items': []},
                    {'id': 2, 'name': 'Store B', 'items': []}
                ]}
                self.assertDictEqual(expected, json.loads(resp.data))

    def test_get_store_list_with_items(self):
        with self.app() as client:
            with self.app_context():
                # Setup
                StoreModel('Store A').save_to_db()
                ItemModel('Item A1', 5.99, 1).save_to_db()
                ItemModel('Item A2', 1.99, 1).save_to_db()
                StoreModel('Store B').save_to_db()
                ItemModel('Item B1', 9.99, 2).save_to_db()

                # Exercise
                path = '/stores'
                headers = {'Authorization': self.access_token}
                resp = client.get(path, headers=headers)

                # Verify
                expected = {'stores': [
                    {
                        'id': 1, 'name': 'Store A',
                        'items': [
                            {'id': 1, 'name': 'Item A1', 'price': 5.99, 'store_id': 1},
                            {'id': 2, 'name': 'Item A2', 'price': 1.99, 'store_id': 1}
                        ]
                    }, {
                        'id': 2, 'name': 'Store B',
                        'items': [{'id': 3, 'name': 'Item B1', 'price': 9.99, 'store_id': 2}]
                    }
                ]}

                self.assertDictEqual(expected, json.loads(resp.data))
