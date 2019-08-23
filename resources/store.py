from flask_restful import Resource

from models.store import StoreModel


class Store(Resource):
    def get(self, name: str):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json(), 200
        return {'message': 'Store not found'}, 404

    def post(self, name):
        if StoreModel.find_by_name(name):
            return {'message': "A store with name '{}' already exists.".format(name)}, 400

        store = StoreModel(name)
        try:
            store.save_to_db()
        except:
            return {'message': 'An error occurred while creating the store.'}, 500

        return store.json(), 201

    def put(self, name):
        # For now the Store has only an unique name and no other properties.
        # TODO: Change this function when the Store has more properties.
        return self.post(name)

    def delete(self, name):
        pass
