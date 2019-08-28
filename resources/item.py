from flask_jwt_extended import jwt_required, fresh_jwt_required
from flask_restful import Resource, reqparse

from models.item import ItemModel


class Item(Resource):
    # Make sure that the 'name' parameter is not replaced
    _parser = reqparse.RequestParser()
    _parser.add_argument(
        'price',
        type=float,
        required=True,
        help="This field cannot be left blank"
    )
    _parser.add_argument(
        'store_id',
        type=int,
        required=True,
        help="Every item needs a store id."
    )

    @jwt_required
    def get(self, name: str):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json(), 200

        return {'message': 'Item not found'}, 404  # Status code NOT FOUND

    @jwt_required
    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': "An item with name '{}' already exists.".format(name)}, 400  # Status code BAD REQUEST

        data = self._parser.parse_args()
        item = ItemModel(name, **data)

        try:
            item.save_to_db()
        except:
            return {'message': 'An error occurred while inserting the item.'}, 500  # Status code INTERNAL SERVER ERROR

        return item.json(), 201  # Status code CREATED

    @jwt_required
    def put(self, name):
        data = Item._parser.parse_args()
        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, **data)
            try:
                item.save_to_db()
            except:
                return {'message': 'An error occurred while inserting the item.'}, 500

            return item.json(), 201
        else:
            item.price = data['price']
            item.store_id = data['store_id']
            try:
                item.save_to_db()
            except:
                return {'message': 'An error occurred while updating the item.'}, 500

        return item.json(), 200

    @fresh_jwt_required
    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return {'message': 'Item deleted'}, 200

        return {'message': 'Item not in db'}, 400


class ItemList(Resource):
    @jwt_required
    def get(self):
        items = [item.json() for item in ItemModel.find_all()]
        return {'items': items}, 200
