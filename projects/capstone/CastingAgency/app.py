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

    @app.after_request
    def after_request(response):
        response.headers.add('Acess-Control-Allow-Headers',
                             'Content-Type, Authorization, true')
        response.headers.add('Acess-Control-Allow-Methods',
                             'GET, POST, PATCH, DELETE, OPTIONS')
        return response

    @app.route('/')
    def welcome_message():
        return 'Welcome to Casting Agency!'

    @app.route('/actors', methods=['GET'])
    @requires_auth('get:actors')
    def get_actors(jwt):
        '''
        This endpoint fetches all the actors
        Parameters:
        jwt: Decoded jwt token which contains the permissions of the user
        Responses:
        200:    An array of actors paginated to 10 actors per page
        422:    Unprocessable request or invalid data in token
        Permissions:
        This endpoint is accessable to Casting Assistants,
            Casting Directors and Executive Producers
        '''
        try:
            actors = Actor.query.all()
            current_actors = paginate_result(request, actors)
            if len(actors) > 0 and len(current_actors) == 0:
                abort(404)
            return jsonify({
                'success': True,
                'actors': current_actors,
                'total_actors': len(actors)
                })
        except Exception as e:
            print(e)
            abort(422)

    @app.route('/movies', methods=['GET'])
    @requires_auth('get:movies')
    def get_movies(jwt):
        '''
        This endpoint fetches all the movies
        Parameters:
        jwt: Decoded jwt token which contains the permissions of the user
        Responses:
        200:    An array of movies paginated to 10 movies per page
        422:    Unprocessable request or invalid data in token
        Permissions:
        This endpoint is accessable to Casting Assistants,
            Casting Directors and Executive Producers
        '''
        try:
            movies = Movie.query.all()
            current_movies = paginate_result(request, movies)
            if len(movies) > 0 and len(current_movies) == 0:
                abort(404)
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
        '''
        This endpoint is to post a new actor
        Parameters:
        jwt: Decoded jwt token which contains the permissions of the user
        Responses:
        200:    New actor is created and returns an array of actors
                paginated to 10 actors per page
        422:    Unprocessable request or invalid data in token
        Permissions:
        This endpoint is accessable only to Casting Directors
            and Executive Producers
        '''
        try:
            data = request.get_json()
            if 'name' not in data or 'age' not in data or 'gender' not in data:
                abort(422)
            actor = Actor(name=data['name'], age=data['age'],
                          gender=data['gender'])
            actor.insert()
            actors = Actor.query.all()
            current_actors = paginate_result(request, actors)
            if len(actors) > 0 and len(current_actors) == 0:
                abort(404)
            return jsonify({
                'success': True,
                'created_actor_id': actor.id,
                'actors': current_actors,
                'total_actors': len(actors)
                })
        except Exception as e:
            print(e)
            abort(422)

    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    def post_movies(jwt):
        '''
        This endpoint is to post a new movie
        Parameters:
        jwt: Decoded jwt token which contains the permissions of the user
        Responses:
        200:    New movie is created and returns an array of movies
                paginated to 10 movies per page
        422:    Unprocessable request or invalid data in token
        Permissions:
        This endpoint is accessable only to Executive Producers
        '''
        try:
            data = request.get_json()
            if 'title' not in data or 'release_date' not in data:
                abort(422)
            new_title = data['title']
            new_release_date = data['release_date']
            movie = Movie(title=new_title, release_date=new_release_date)
            movie.insert()
            movies = Movie.query.all()
            current_movies = paginate_result(request, movies)
            if len(movies) > 0 and len(current_movies) == 0:
                abort(404)
            return jsonify({
                'success': True,
                'created_movie_id': movie.id,
                'movies': current_movies,
                'total_movies': len(movies)
                })
        except Exception as e:
            print(e)
            abort(422)

    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    @requires_auth('patch:actors')
    def edit_actors(jwt, actor_id):
        '''
        This endpoint is to edit an existing actor
        Parameters:
        jwt: Decoded jwt token which contains the permissions of the user
        actor_id: id of actor to be edited
        Responses:
        200:    Actor is edited and returns an array of actors
                paginated to 10 actors per page
        422:    Unprocessable request or invalid data in token
        Permissions:
        This endpoint is accessable only to Casting Directors
            and Executive Producers
        '''
        try:
            actor = Actor.query.get(actor_id)
            if actor:
                data = request.get_json()
                if 'name' in data:
                    actor.name = data['name']
                if 'age' in data:
                    actor.age = data['age']
                if 'gender' in data:
                    actor.gender = data['gender']
                actor.update()
                actors = Actor.query.all()
                current_actors = paginate_result(request, actors)
                if len(actors) > 0 and len(current_actors) == 0:
                    abort(404)
                return jsonify({
                    'success': True,
                    'edited_actor_id': actor.id,
                    'actors': current_actors,
                    'total_actors': len(actors)
                })
            else:
                abort(404)
        except Exception as e:
            print(e)
            abort(422)

    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    @requires_auth('patch:movies')
    def edit_movies(jwt, movie_id):
        '''
        This endpoint is to edit an existing movie
        Parameters:
        jwt: Decoded jwt token which contains the permissions of the user
        movie_id: id of movie to be edited
        Responses:
        200:    Movie is edited and returns an array of movies
                paginated to 10 movies per page
        422:    Unprocessable request or invalid data in token
        Permissions:
        This endpoint is accessable only to Casting Directors
            and Executive Producers
        '''
        try:
            movie = Movie.query.get(movie_id)
            if movie:
                data = request.get_json()
                if 'title' in data:
                    movie.title = data['title']
                if 'release_date' in data:
                    movie.release_date = data['release_date']
                movie.update()
                movies = Movie.query.all()
                current_movies = paginate_result(request, movies)
                if len(movies) > 0 and len(current_movies) == 0:
                    abort(404)
                return jsonify({
                    'success': True,
                    'edited_movie_id': movie.id,
                    'movies': current_movies,
                    'total_movies': len(movies)
                    })
            else:
                abort(404)
        except Exception as e:
            print(e)
            abort(422)

    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actors(jwt, actor_id):
        '''
        Parameters:
        jwt: Decoded jwt token which contains the permissions of the user
        actor_id: id of actor to be deleted
        Responses:
        200:    Actor is deleted and returns an array of actors
                paginated to 10 actors per page
        422:    Unprocessable request or invalid data in token
        Permissions:
        This endpoint is accessable only to Casting Directors
            and Executive Producers
        '''
        try:
            actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
            if actor:
                actor.delete()
                actors = Actor.query.all()
                current_actors = paginate_result(request, actors)
                if len(actors) > 0 and len(current_actors) == 0:
                    abort(404)
                return jsonify({
                    'success': True,
                    'deleted_actor_id': actor.id,
                    'actors': current_actors,
                    'total_actors': len(actors)
                })
            else:
                abort(404)
        except Exception as e:
            print(e)
            abort(422)

    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movies(jwt, movie_id):
        '''
        Parameters:
        jwt: Decoded jwt token which contains the permissions of the user
        movie_id: id of movie to be deleted
        Responses:
        200:    Movie is deleted and returns an array of movies
                paginated to 10 movies per page
        422:    Unprocessable request or invalid data in token
        Permissions:
        This endpoint is accessable only to Executive Producers
        '''
        try:
            movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
            if movie:
                movie.delete()
                movies = Movie.query.all()
                current_movies = paginate_result(request, movies)
                if len(movies) > 0 and len(current_movies) == 0:
                    abort(404)
                return jsonify({
                    'success': True,
                    'deleted_movie_id': movie.id,
                    'movies': current_movies,
                    'total_movies': len(movies)
                })
            else:
                abort(404)
        except Exception as e:
            print(e)
            abort(422)

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': "Bad request"
            }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': "Not found"
            }), 404

    @app.errorhandler(405)
    def not_allowed(error):
        return jsonify({
            'success': False,
            'error': 405,
            'message': "Method not allowed"
            }), 405

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': "Unprocessable"
            }), 422

    @app.errorhandler(500)
    def internal(error):
        return jsonify({
            'success': False,
            'error': 500,
            'message': "Internal server error"
            }), 500

    @app.errorhandler(AuthError)
    def unauthorized(error):
        return jsonify({
            'success': False,
            'error': 401,
            'message': 'Unauthorized'
            }), 401

    return app


APP = create_app()


if __name__ == '__main__':
    APP.run(debug=True)
