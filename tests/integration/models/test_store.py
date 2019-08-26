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
