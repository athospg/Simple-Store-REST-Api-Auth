from flask_restful import Resource

from models.store import StoreModel


class Item(Resource):
    def get(self, name: str):
        pass

    def post(self, name):
        pass

    def put(self, name):
        pass

    def delete(self, name):
        pass
