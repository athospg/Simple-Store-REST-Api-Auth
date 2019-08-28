from flask_jwt_extended import create_access_token, create_refresh_token
from flask_restful import Resource, reqparse

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
    pass


class UserLogout(Resource):
    pass
