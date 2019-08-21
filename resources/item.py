from flask_restful import Resource

from models.item import ItemModel


class Item(Resource):
    def get(self, name: str):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json(), 200

        return {'message': 'Item not found'}, 404

    def post(self, name):
        pass

    def put(self, name):
        pass

    def delete(self, name):
        pass
