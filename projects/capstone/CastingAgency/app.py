import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from models import setup_db, Movie, Actor
from auth import AuthError, requires_auth


RESULT_PER_PAGE = 10


def paginate_result(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * RESULT_PER_PAGE
    end = start + RESULT_PER_PAGE

    items = [item.format() for item in selection]
    current_items = items[start:end]
    return current_items


def create_app(test_config=None):
	# create and configure the app
	app = Flask(__name__)
	setup_db(app)
	CORS(app)

	@app.route('/actors',methods=['GET'])
	@requires_auth('get:actors')
	def get_actors(jwt):
		try:
			actors = Actor.query.all()
			current_actors = paginate_result(request, actors)
			return jsonify({
				'success': True,
				'actors': current_actors,
				'total_actors': len(actors)
			})
		except Exception as e:
			print(e)
			abort(422)

	@app.route('/movies',methods=['GET'])
	@requires_auth('get:movies')
	def get_movies(jwt):
		try:
			movies = Movie.query.all()
			current_movies = paginate_result(request, movies)
			return jsonify({
				'success': True,
				'movies': current_movies,
				'total_movies': len(movies)
			})
		except Exception as e:
			print(e)
			abort(422)
			
	@app.route('/actors', methods=['POST'])
	@requires_auth('post:actors')
	def post_actors(jwt):
		try:
			data = request.get_json()
			if 'name' not in data or 'age' not in data or 'gender' not in data:
				abort(422)
			actor = Actor(name=data['name'],age=data['age'],gender=data['gender'])
			actor.insert()
		except Exception as e:
			print(e)
			abort(422)

	return app

APP = create_app()


if __name__ == '__main__':
	APP.run(debug=True)