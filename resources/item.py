import sqlite3

from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "name", type=str, required=True, help="This field cannot be left blank!"
    )
    parser.add_argument(
        "price", type=float, required=True, help="This field cannot be left blank!"
    )
    parser.add_argument(
        "store_id", type=int, required=True, help="This field cannot be left blank!"
    )

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)

        if item:
            return item.json(), 201
        else:
            return {"message": "Item not found"}, 404

    def post(self, name):

        data = Item.parser.parse_args()

        if ItemModel.find_by_name(name=data["name"]):
            return {"message": "item with name is already exist"}

        item = ItemModel(data["name"], data["price"], data['store_id'])

        try:
            item.save_to_db()
        except:
            return {"message": "An exception raised"}, 500

        return {"message": "Item was successfully created"}, 201

    # @jwt_required()
    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return {"message": "Item deleted"}

    # @jwt_required()
    def put(self, name):
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(data["name"], data["price"], data['store_id'])
        else:
            item.price = data["price"]
            item.store_id = data['store_id']

        item.save_to_db()

        return item.json()


class ItemList(Resource):
    def get(self):
        return {"items": list(map(lambda x: x.json(), ItemModel.query.all()))}
