import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from models import setup_db, Movie, Actor
from auth import AuthError, requires_auth


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
			return jsonify({
				'success': True,
				'actors': [actor.format() for actor in actors]
			})
		except Exception as e:
			print(e)
			abort(422)

	@app.route('/movies',methods=['GET'])
	@requires_auth('get:movies')
	def get_movies(jwt):
		try:
			movies = Movie.query.all()
			return jsonify({
				'success': True,
				'actors': [movie.format() for movie in movies]
			})
		except Exception as e:
			print(e)
			abort(422)
			

	return app

APP = create_app()


if __name__ == '__main__':
	APP.run(host='0.0.0.0', port=8080, debug=True)