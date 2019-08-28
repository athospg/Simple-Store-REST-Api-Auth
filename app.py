import os

from flask import Flask
from flask_jwt_extended import JWTManager
from flask_restful import Api

from blacklist import BLACKLIST
from resources.item import Item, ItemList
from resources.store import Store, StoreList
from resources.user import UserRegister, UserLogin, UserLogout, User, TokenRefresh

app = Flask(__name__)

app.config['DEBUG'] = True

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
app.secret_key = 'Key_McKeyFace'  # app.config['JWT_SECRET_KEY']

api = Api(app)

jwt = JWTManager(app)


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    """
    Checks if a user is in the blacklist (logged out, etc.)
    Needs:
        app.config['JWT_BLACKLIST_ENABLED'] = True
        app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']  # To block both cases
    """
    return decrypted_token['jti'] in BLACKLIST


# User related resources
api.add_resource(UserRegister, '/register')
api.add_resource(UserLogin, '/login')
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(TokenRefresh, '/refresh')
api.add_resource(UserLogout, '/logout')

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
