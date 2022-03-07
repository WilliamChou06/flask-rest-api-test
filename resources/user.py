import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel


class User(Resource):
    @classmethod
    def get(cls, user_id):
        user = UserModel.find_by_id(user_id)

        if not user:
            return {'message': 'No user found'}, 404

        return user.json(), 200

    @classmethod
    def delete(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': 'User does not exist'}, 404

        user.delete_from_db()
        return {'message': 'User deleted successfully'}, 200


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True,
                        help="This field is required")
    parser.add_argument('password', type=str, required=True,
                        help="This field is required")

    def post(self):
        data = UserRegister.parser.parse_args()

        user_exists = UserModel.find_by_username(data['username'])

        if user_exists:
            return {"message": "User already exists"}, 409

        try:
            user = UserModel(**data).save_user_to_db()
        except:
            return {"message": "User creation error"}, 500

        return {"message": "User created successfully"}, 201
