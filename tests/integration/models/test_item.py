from models.item import ItemModel
from models.store import StoreModel
from tests.base_test import BaseTest


class ItemTest(BaseTest):
    def test_crud(self):
        """
        CRUD: Create, Read, Update and Delete.
        These are the four major and basic functions of persistent storage.
        """
        with self.app_context():
            # Setup
            StoreModel('test').save_to_db()
            item = ItemModel('test', 19.99, 1)

            # Exercise

            # Verify
            self.assertIsNone(ItemModel.find_by_name('test'),
                              "Found an item with name {}, but expected not to.".format(item.name))

            # Exercise
            item.save_to_db()

            # Verify
            self.assertIsNotNone(ItemModel.find_by_name('test'))

            # Exercise
            item.delete_from_db()

            # Verify
            self.assertIsNone(ItemModel.find_by_name('test'))

    def test_store_relationship(self):
        with self.app_context():
            # Setup
            store = StoreModel('Store 1')
            item = ItemModel('test', 19.99, 1)

            # Exercise
            store.save_to_db()
            item.save_to_db()

            # Verify
            self.assertEqual('Store 1', item.store.name)
