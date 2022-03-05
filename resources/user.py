import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel


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

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        insert_query = "INSERT INTO users VALUES (NULL, ?, ?)"
        cursor.execute(insert_query, (data['username'], data['password']))

        connection.commit()
        connection.close()

        return {"message": "User created successfully"}, 201
