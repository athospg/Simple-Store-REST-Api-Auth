from unittest import TestCase

# noinspection PyUnresolvedReferences
from models.item import ItemModel
from models.store import StoreModel


class StoreTest(TestCase):
    def test_create_store(self):
        # Setup

        # Exercise
        store = StoreModel('Store A')

        # Verify
        self.assertEqual('Store A', store.name)

    def test_store_json(self):
        # Setup

        # Exercise
        store = StoreModel('Test Store')

        # Verify
        expected = {'id': None, 'name': 'Test Store', 'items': []}
        self.assertEqual(expected, store.json())
