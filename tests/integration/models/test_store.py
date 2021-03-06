from models.item import ItemModel
from models.store import StoreModel
from tests.base_test import BaseTest


class StoreTest(BaseTest):
    def test_crud(self):
        """
        CRUD: Create, Read, Update and Delete.
        These are the four major and basic functions of persistent storage.
        """
        with self.app_context():
            # Setup
            store = StoreModel('test')

            # Exercise

            # Verify
            self.assertIsNone(StoreModel.find_by_name('test'))

            # Exercise
            store.save_to_db()

            # Verify
            self.assertIsNotNone(StoreModel.find_by_name('test'))

            # Exercise
            store.delete_from_db()

            # Verify
            self.assertIsNone(StoreModel.find_by_name('test'))

    def test_create_store_empty_items(self):
        store = StoreModel('test')

        self.assertListEqual([], store.items.all(),
                             "The store's items length was not 0 even though no items were added.")

    def test_item_relationship(self):
        with self.app_context():
            # Setup
            store = StoreModel('test')
            item = ItemModel('Item A', 19.99, 1)

            # Exercise
            store.save_to_db()
            item.save_to_db()

            # Verify
            self.assertEqual(1, store.items.count())
            self.assertEqual('Item A', store.items.first().name)

    def test_store_json_with_item(self):
        with self.app_context():
            # Setup
            store = StoreModel('test')
            item = ItemModel('Item A', 19.99, 1)

            # Exercise
            store.save_to_db()
            item.save_to_db()

            # Verify
            expected = {
                'id': 1,
                'name': 'test',
                'items': [{'id': 1, 'name': 'Item A', 'price': 19.99, 'store_id': 1}]
            }
            self.assertDictEqual(expected, store.json())
