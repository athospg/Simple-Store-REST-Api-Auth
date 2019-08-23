from flask_restful import Resource

from models.store import StoreModel


class Store(Resource):
    def get(self, name: str):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json(), 200
        return {'message': 'Store not found'}, 404

    def post(self, name):
        pass

    def put(self, name):
        pass

    def delete(self, name):
        pass
