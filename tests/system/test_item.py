import json

from models.item import ItemModel
from models.store import StoreModel
from tests.base_test import BaseTest


class ItemTest(BaseTest):

    def test_get_item_not_found(self):
        with self.app() as client:
            with self.app_context():
                # Setup

                # Exercise
                path = '/item/test'
                resp = client.get(path)

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
                resp = client.get(path)

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
                headers = {'Content-Type': 'application/json'}
                data = json.dumps({'price': 17.99, 'store_id': 1})
                resp = client.post(path, headers=headers, data=data)

                # Verify
                expected = {'id': 1, 'name': 'test', 'price': 17.99, 'store_id': 1}

                self.assertEqual(201, resp.status_code)
                self.assertDictEqual(expected, json.loads(resp.data))
