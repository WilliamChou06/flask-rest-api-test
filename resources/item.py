import sqlite3
from flask_restful import Resource, Api, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    def get(self, name):
        item = ItemModel.find_by_name(name)

        if item:
            return item.json(), 200

        return {'message': 'Item not found'}, 404

    @jwt_required()
    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': "An item with name '{}' already exists.".format(name)}, 409

        data = Item.parser.parse_args()
        item = ItemModel(name, data['price'])

        try:
            item.insert()
        except:
            return {'message': 'An error has occurred'}, 500

        return item.json(), 201

    @jwt_required()
    def delete(self, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = 'DELETE FROM items WHERE name=?'
        cursor.execute(query, (name,))

        connection.commit()
        connection.close()

        return {'message': 'Item deleted'}, 200

    @jwt_required()
    def put(self, name):
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)
        formatted_item = ItemModel(name, data['price'])

        if item is None:
            try:
                formatted_item.insert()
            except:
                return {'message': 'Error inserting item'}, 500
        else:
            try:
                formatted_item.update()
            except:
                return {'message': 'Error updating item'}, 500

        return formatted_item.json(), 200


class ItemList(Resource):
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = 'SELECT * FROM items'
        results = cursor.execute(query)
        rows = results.fetchall()
        items = list(map(
            lambda item: {'name': item[0], 'price': item[1]}, rows))

        connection.commit()
        connection.close()

        return {'items': items}
