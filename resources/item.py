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

    def get(self, name: str):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json(), 200

        return {'message': 'Item not found'}, 404

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

    def put(self, name):
        pass

    def delete(self, name):
        pass
