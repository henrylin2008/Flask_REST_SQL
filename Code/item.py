class Item(Resource):
	# ensure correct data is enter
	parser = reqparse.RequestParser()
	parser.add_argument('price',
						type=float,
						required=True,
						help="This field cannot be left blank!"
						)


	@jwt_required()
	def get(self, name):
		item = next(filter(lambda x: x['name'] == name, items), None)
		return {'item': item}, 200 if item is not None else 404


	def post(self, name):
		#Error check
		if next(filter(lambda x: x['name'] == name, items), None) is not None:
			return {'message': "An item with name '{}' already exist".format(name)}, 400

		data = Item.parser.parse_args()

		item = {'name': name, 'price': data['price']}
		items.append(item)
		return item, 201


	def delete(self, name):
		global items
		items = list(filter(lambda x: x['name'] != name, items))
		return {'message': 'Item deleted'}


	def put(self, name):
		data = Item.parser.parse_args()

		item = next(filter(lambda x: x['name'] == name, items), None)
		if item is None:
			item = {'name': name, 'price': data['price']}
			items.append(item)
		else:
			item.update(data)
		return item


class ItemList(Resource):
	def get(self):
		return {'items': items}