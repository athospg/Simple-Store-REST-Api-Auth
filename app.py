from flask import Flask
from flask_restful import Api

from resources.item import Item, ItemList
from resources.store import Store, StoreList

app = Flask(__name__)

app.config['DEBUG'] = True

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True

api = Api(app)

# Store related resources
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')

# Item related resources
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    from db import db

    if app.config['DEBUG']:
        @app.before_first_request
        def create_tables():
            db.create_all()

    db.init_app(app)
    app.run()
