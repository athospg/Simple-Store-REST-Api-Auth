import json

from models.item import ItemModel
from models.store import StoreModel
from tests.base_test import BaseTest


class StoreTest(BaseTest):

    def test_create_store(self):
        with self.app() as client:
            with self.app_context():
                # Setup

                # Exercise
                path = '/store/test'
                resp = client.post(path)

                # Verify
                expected = {'id': 1, 'name': 'test', 'items': []}

                self.assertEqual(201, resp.status_code)
                self.assertDictEqual(expected, json.loads(resp.data))
                self.assertIsNotNone(StoreModel.find_by_name('test'))

    def test_get_store_not_found(self):
        with self.app() as client:
            with self.app_context():
                # Setup

                # Exercise
                path = '/store/test'
                resp = client.get(path)

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
                resp = client.get(path)

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
                resp = client.get(path)

                # Verify
                expected = {
                    'id': 1,
                    'name': 'Store 1',
                    'items': [{'id': 1, 'name': 'Item A', 'price': 19.99, 'store_id': 1}]
                }

                self.assertEqual(200, resp.status_code)
                self.assertDictEqual(expected, json.loads(resp.data))
