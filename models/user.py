import sqlite3
from db import db


class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    password = db.Column(db.String(80))

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
