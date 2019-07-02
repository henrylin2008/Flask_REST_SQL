import sqlite3
from flask_restful import Resource, reqparse

class User:
	def __init__(self, _id, username, password): 
		self.id = _id
		self.username = username
		self.password = password


	@classmethod
	def find_by_username(cls, username):
		connection = sqlite3.connect('data.db')
		cursor = connection.cursor()

		query = "SELECT * FROM {table} WHERE username=?".format(table=cls.TABLE_NAME)
		result = cursor.execute(query, (username,))
		row = result.fetchone()
		if row:
			user = cls(*row)
		else:
			user = None

		connection.close()
		return user


	@classmethod
	def find_by_id(cls, _id):
		connection = sqlite3.connect('data.db')
		cursor = connection.cursor()

		query = "SELECT * FROM {table} WHERE id=?".format(table=cls.TABLE_NAME)
		result = cursor.execute(query, (_id,))
		row = result.fetchone()
		if row:
			user = cls(*row)
		else:
			user = None

		connection.close()
		return user


class UserRegister(Resource):

	parser = reqparse.RequestParser()
	parser.add_argument('username',
			type=str,
			required=True,
			help="This field cannot be blank."

	)
	parser.add_argument('password',
			type=str,
			required=True,
			help="This field cannot be blank."
	)


	def post(self):
		data = UserRegister.parser.parse_args()

		if User.find_by_username(data['username']): ## if username is not none
			return {"message": "A user with that username already exist"}, 400

		connection = sqlite3.connect('data.db')
		cursor = connection.cursor()

		query = "INSERT INTO users VALUES (NULL, ?, ?)"
		cursor.execute(query, (data['username'], data['password']))

		connection.commit()
		connection.close()

		return {"message": "User created successfully."}, 201

