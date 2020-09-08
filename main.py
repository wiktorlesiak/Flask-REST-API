from flask import Flask, request
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class DataModel(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	city = db.Column(db.String(45), nullable=False)
	population = db.Column(db.Integer, nullable=False)
	weather = db.Column(db.String(45), nullable=False)

	def __repr__(self):
		return f"data(city = {city}, population = {population}, weather = {weather})"

# db.create_all()

data_put_args = reqparse.RequestParser()
data_put_args.add_argument("city", type=str, help="Name of the city is required", required = True)
data_put_args.add_argument("population", type=int, help="Population of the video is required", required = True)
data_put_args.add_argument("weather", type=str, help="Weather of the city is required", required = True)

data_uptade_args = reqparse.RequestParser()
data_uptade_args.add_argument("city", type=str, help="Name of the city is required")
data_uptade_args.add_argument("population", type=int, help="Population of the video is required")
data_uptade_args.add_argument("weather", type=str, help="Weather of the city is required")

resource_fields = {
	'id': fields.Integer,
	'city': fields.String,
	'population': fields.Integer,
	'weather': fields.String
}

class Data(Resource):
	@marshal_with(resource_fields)
	def get(self, city_id):
		result = DataModel.query.filter_by(id=city_id).first()
		if not result:
			abort(404, message="Could not find city with that id")
		return result

	@marshal_with(resource_fields)	
	def put(self, city_id):
		args = data_put_args.parse_args()
		result = DataModel.query.filter_by(id=city_id).first()
		if result:
			abort(409, message="City id taken...")

		data = DataModel(id=city_id, city=args['city'], population=args['population'], weather=args['weather'])
		db.session.add(data)
		db.session.commit()

		return data, 201

	@marshal_with(resource_fields)
	def patch(self, city_id):
		args = data_uptade_args.parse_args()
		result = DataModel.query.filter_by(id=city_id).first()
		if not result:
			abort(409, message="City doesn't exist, cannot update")

		if args['city']:
			result.city = args['city']
		if args['population']:
			result.population = args['population']
		if args['weather']:
			result.weather = args['weather']

		db.session.commit()

		return result

	@marshal_with(resource_fields)
	def delete(self, city_id):
		result = DataModel.query.filter_by(id=city_id).first()
		del data

		return data, 204


api.add_resource(Data, "/city/<int:city_id>")

if __name__ == "__main__":
	app.run(debug=True)

