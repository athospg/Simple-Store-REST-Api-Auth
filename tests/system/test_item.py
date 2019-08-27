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
