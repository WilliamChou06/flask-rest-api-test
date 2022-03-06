from flask_restful import Resource
from models.store import StoreModel


class Store(Resource):
    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json(), 200
        return {'message': 'Store not found'}, 404

    def post(self, name):
        if StoreModel.find_by_name(name):
            return {'message': f'Store with name {name} already exists'}, 404

        try:
            store = StoreModel(name)
            store.save_to_db()
        except:
            return {'message': 'Store creation error'}, 500

        return store.json(), 201

    def delete(self, name):
        item = StoreModel.find_by_name(name).delete_from_db()

        return {'message': 'Store deleted successfully'}, 200


class StoreList(Resource):
    def get(self):
        return {'items': [item.json() for item in StoreModel.query.all()]}
