import json

from models.store import StoreModel
from tests.base_test import BaseTest


class StoreTest(BaseTest):

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
