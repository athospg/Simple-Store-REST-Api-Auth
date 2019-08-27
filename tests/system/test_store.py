import json

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
