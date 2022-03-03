from flask_restful import Resource, reqparse
import sqlite3


class User(object):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls, username):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        find_query = "SELECT * FROM users WHERE username=?"

        result = cursor.execute(find_query, (username,))
        row = result.fetchone()

        if row:
            print(row)
            user = cls(*row)

        else:
            user = None

        connection.close()
        return user

    @classmethod
    def find_by_id(cls, _id):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        find_query = "SELECT * FROM users WHERE id=?"

        result = cursor.execute(find_query, (_id,))
        row = result.fetchone()

        if row:
            print(row)
            user = cls(*row)

        else:
            user = None

        connection.close()
        return user


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True,
                        help="This field is required")
    parser.add_argument('password', type=str, required=True,
                        help="This field is required")

    def post(self):
        data = UserRegister.parser.parse_args()

        user_exists = User.find_by_username(data['username'])

        if user_exists:
            return {"message": "User already exists"}, 409

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        insert_query = "INSERT INTO users VALUES (NULL, ?, ?)"
        cursor.execute(insert_query, (data['username'], data['password']))

        connection.commit()
        connection.close()

        return {"message": "User created successfully"}, 201
