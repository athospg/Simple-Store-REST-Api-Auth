import json

from models.item import ItemModel
from models.store import StoreModel
from models.user import UserModel
from tests.base_test import BaseTest


# noinspection DuplicatedCode
class ItemTest(BaseTest):
    def setUp(self):
        super(ItemTest, self).setUp()
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

    def test_get_item_no_auth(self):
        with self.app() as client:
            with self.app_context():
                # Setup

                # Exercise
                path = '/item/test'
                resp = client.get(path)

                # Verify
                self.assertEqual(401, resp.status_code)

    def test_get_item_not_found(self):
        with self.app() as client:
            with self.app_context():
                # Setup

                # Exercise
                path = '/item/test'
                headers = {'Authorization': self.access_token}
                resp = client.get(path, headers=headers)

                # Verify
                self.assertEqual(404, resp.status_code)

    def test_get_item(self):
        with self.app() as client:
            with self.app_context():
                # Setup
                StoreModel('test').save_to_db()
                ItemModel('test', 19.99, 1).save_to_db()

                # Exercise
                path = '/item/test'
                headers = {'Authorization': self.access_token}
                resp = client.get(path, headers=headers)

                # Verify
                expected = {'id': 1, 'name': 'test', 'price': 19.99, 'store_id': 1}

                self.assertEqual(200, resp.status_code)
                self.assertDictEqual(expected, json.loads(resp.data))

    def test_create_item(self):
        with self.app() as client:
            with self.app_context():
                # Setup
                StoreModel('test').save_to_db()

                # Exercise
                path = '/item/test'
                headers = {'Content-Type': 'application/json',
                           'Authorization': self.access_token}
                data = json.dumps({'price': 17.99, 'store_id': 1})
                resp = client.post(path, headers=headers, data=data)

                # Verify
                expected = {'id': 1, 'name': 'test', 'price': 17.99, 'store_id': 1}

                self.assertEqual(201, resp.status_code)
                self.assertDictEqual(expected, json.loads(resp.data))

    def test_create_duplicate_item(self):
        with self.app() as client:
            with self.app_context():
                # Setup
                StoreModel('test').save_to_db()
                ItemModel('test', 17.99, 1).save_to_db()

                # Exercise
                path = '/item/test'
                headers = {'Content-Type': 'application/json',
                           'Authorization': self.access_token}
                data = json.dumps({'price': 17.99, 'store_id': 1})
                resp = client.post(path, headers=headers, data=data)

                # Verify
                expected = {'message': 'An item with name \'test\' already exists.'}

                self.assertEqual(400, resp.status_code)
                self.assertDictEqual(expected, json.loads(resp.data))

    def test_put_create_item(self):
        with self.app() as client:
            with self.app_context():
                # Setup
                StoreModel('test').save_to_db()

                # Exercise
                path = '/item/test'
                headers = {'Content-Type': 'application/json',
                           'Authorization': self.access_token}
                data = json.dumps({'price': 17.99, 'store_id': 1})
                resp = client.put(path, headers=headers, data=data)

                # Verify
                expected = {'id': 1, 'name': 'test', 'price': 17.99, 'store_id': 1}

                self.assertEqual(201, resp.status_code)
                self.assertDictEqual(expected, json.loads(resp.data))
                self.assertEqual(17.99, ItemModel.find_by_name('test').price)

    def test_update_item(self):
        with self.app() as client:
            with self.app_context():
                # Setup
                StoreModel('test').save_to_db()
                ItemModel('test', 5.99, 1).save_to_db()

                # Exercise
                path = '/item/test'
                headers = {'Content-Type': 'application/json',
                           'Authorization': self.access_token}
                data = json.dumps({'price': 19.99, 'store_id': 1})
                resp = client.put(path, headers=headers, data=data)

                # Verify
                expected = {'id': 1, 'name': 'test', 'price': 19.99, 'store_id': 1}

                self.assertEqual(200, resp.status_code)
                self.assertDictEqual(expected, json.loads(resp.data))
                self.assertEqual(19.99, ItemModel.find_by_name('test').price)

    def test_delete_item(self):
        with self.app() as client:
            with self.app_context():
                # Setup
                StoreModel('test').save_to_db()
                ItemModel('test', 19.99, 1).save_to_db()

                # Exercise
                path = '/item/test'
                headers = {'Authorization': self.access_token}
                resp = client.delete(path, headers=headers)

                # Verify
                expected = {'message': 'Item deleted'}

                self.assertEqual(200, resp.status_code)
                self.assertDictEqual(expected, json.loads(resp.data))

    def test_item_list(self):
        with self.app() as client:
            with self.app_context():
                # Setup
                StoreModel('Store1').save_to_db()
                ItemModel('Item1', 5.99, 1).save_to_db()
                ItemModel('Item2', 1.99, 1).save_to_db()
                StoreModel('Store2').save_to_db()
                ItemModel('Item3', 9.99, 2).save_to_db()

                # Exercise
                path = '/items'
                headers = {'Authorization': self.access_token}
                resp = client.get(path, headers=headers)

                # Verify
                expected = {'items': [
                    {'id': 1, 'name': 'Item1', 'price': 5.99, 'store_id': 1},
                    {'id': 2, 'name': 'Item2', 'price': 1.99, 'store_id': 1},
                    {'id': 3, 'name': 'Item3', 'price': 9.99, 'store_id': 2}
                ]}
                self.assertDictEqual(expected, json.loads(resp.data))
