from unittest import TestCase

from models.item import ItemModel
# noinspection PyUnresolvedReferences
from models.store import StoreModel


class ItemTest(TestCase):
    def test_create_item(self):
        # Setup

        # Exercise
        item = ItemModel('test', 13.99, 3)

        # Verify
        self.assertEqual('test', item.name)
        self.assertEqual(13.99, item.price)
        self.assertEqual(3, item.store_id)

    def test_item_json(self):
        # Setup

        # Exercise
        item = ItemModel('Test Item', 1.99, 1)

        # Verify
        expected = {'id': None, 'name': 'Test Item', 'price': 1.99, 'store_id': 1}
        self.assertEqual(expected, item.json())
