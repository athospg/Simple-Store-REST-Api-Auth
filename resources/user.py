from flask_jwt_extended import (
    jwt_required, create_access_token, create_refresh_token, jwt_refresh_token_required, get_jwt_identity,
    fresh_jwt_required,
    get_raw_jwt)
from flask_restful import Resource, reqparse

from blacklist import BLACKLIST
from models.user import UserModel

_user_parser = reqparse.RequestParser()
_user_parser.add_argument(
    'username',
    type=str,
    required=True,
    help="This field cannot be left blank"
)
_user_parser.add_argument(
    'password',
    type=str,
    required=True,
    help="This field cannot be left blank"
)


class UserRegister(Resource):
    def post(self):
        data = _user_parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {'message': 'A user with that username already exists.'}, 400

        user = UserModel(**data)
        user.save_to_db()

        return {'message': 'User created successfully.'}, 201


class UserLogin(Resource):
    @classmethod
    def post(cls):
        # get data from parser
        data = _user_parser.parse_args()

        # find user in database
        user = UserModel.find_by_username(data['username'])

        # check password
        # create access token
        # create refresh token
        if user and user.password == data['password']:
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(identity=user.id)
            return {
                       'access_token': access_token,
                       'refresh_token': refresh_token
                   }, 200

        return {'message': 'Invalid credentials'}, 401


class User(Resource):
    @classmethod
    @jwt_required
    def get(cls, user_id: int):
        user = UserModel.find_by_id(user_id)
        if user:
            return user.json(), 200
        return {'message': 'User not found'}, 404

    @classmethod
    @fresh_jwt_required
    def delete(cls, user_id: int):
        user = UserModel.find_by_id(user_id)
        if user:
            user.delete_from_db()
            return {'message': 'User deleted'}, 200
        return {'message': 'User not found'}, 404


class UserLogout(Resource):
    @jwt_required
    def post(self):
        # Every time a user logs in an unique 'JWT ID' is created.
        # In order to logout the user we need to blacklist this id and not the
        # 'USER ID', otherwise they wouldn't be able to login again.
        jti = get_raw_jwt()['jti']
        BLACKLIST.add(jti)
        return {'message': 'Successfully logged out.'}, 200


class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {'access_token': new_token}, 200
