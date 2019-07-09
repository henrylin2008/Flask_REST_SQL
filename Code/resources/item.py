from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_claims
from models.item import ItemModel

class Item(Resource):
	# ensure correct data is enter
	parser = reqparse.RequestParser()
	parser.add_argument('price',
						type=float,
						required=True,
						help="This field cannot be left blank!"
						)
	parser.add_argument('store_id',
						type=int,
						required=True,
						help="Every item needs a store id."
						)
	@jwt_required
	def get(self, name):
		item = ItemModel.find_by_name(name)
		if item:
			return item.json()
		return {'message': 'Item not found'}, 404

	def post(self, name):
		#Error check
		if ItemModel.find_by_name(name):
			return {'message': "An item with name '{}' already exist".format(name)}, 400

		data = Item.parser.parse_args()

		item = ItemModel(name, **data) ## **data = data['price'], data['store_id']

		try:
			item.save_to_db()
		except:
			return {"message": "An error occurred inserting the item."}, 500 # server error

		return item.json(), 201

	@jwt_required
	def delete(self, name):
		claims = get_jwt_claims()
		if not claims['is_admin']:
			return{'message': 'Admin privilege required.'}, 401

		item = ItemModel.find_by_name(name)
		if item:
			item.delete_from_db()

		return {'message': 'Item deleted'}

	def put(self, name):
		data = Item.parser.parse_args()

		item = ItemModel.find_by_name(name)

		if item is None:
			item = ItemModel(name, **data) ## **data = data['price'], data['store_id']
		else:
			item.price = data['price']

		item.save_to_db()

		return item.json()


class ItemList(Resource):
	def get(self):
		return {'items': [item.json() for item in ItemModel.find_all()]}
		## same as 'items': list(map(lambda x: x.json(), ItemModel.query.all()))
