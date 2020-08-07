# pylint: disable=missing-class-docstring, missing-function-docstring, global-statement, bare-except

from flask_restful import Resource
from models.store import StoreModel


class Store(Resource):
    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        return {'message': 'Store not found'}, 404

    def post(self, name):
        if StoreModel.find_by_name(name):
            return {'message': "An store with name '{}' already exists.".format(name)}, 400
        store = StoreModel(name=name)
        try:
            store.save_to_db()
        except:
            return {"message": "An error occurred inserting the item."}, 500

        return store.json(), 201

    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            for item in store.items:
                item.delete_from_db()
            store.delete_from_db()

        return {'message': 'Store deleted'}

class StoreList(Resource):
    def get(self):
        return {'store': [x.json() for x in StoreModel.query.all()]}
