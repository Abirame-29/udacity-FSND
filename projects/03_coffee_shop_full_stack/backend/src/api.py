import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers',
                         'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods',
                         'GET,PUT,POST,DELETE,OPTIONS')
    return response


'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
'''
# db_drop_and_create_all()

# ROUTES


@app.route('/drinks', methods=['GET'])
def get_drinks():
    '''
    This endpoint fetches all the drinks
    Responses:
        200:    An array of drinks in short form
        422:    Unprocessable request
    Permissions:
        This endpoint is available to public
    '''
    try:
        drinks = Drink.query.all()
        return jsonify({
            'success': True,
            'drinks': [drink.short() for drink in drinks]
        })
    except Exception as e:
        print(e)
        abort(422)


@app.route('/drinks-detail', methods=['GET'])
@requires_auth('get:drinks-detail')
def get_drinks_detail(jwt):
    '''
    This endpoint fetches all the drinks and its details
    Responses:
        200:    An array of drinks in long form
        422:    Unprocessable request
    Permissions:
        This endpoint is accessable to Baristas and Managers
    '''
    try:
        drinks = Drink.query.all()
        if len(drinks) == 0:
            abort(404)
        return jsonify({
            'success': True,
            'drinks': [drink.long() for drink in drinks]
        })
    except Exception as e:
        print(e)
        abort(422)


@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def post_drinks(jwt):
    '''
    This endpoint is to post a new drink
    Parameters:
        jwt: Decoded jwt token which contains the title
             and recipe of the new drink
    Responses:
        200:    New drink which is created in long form
        422:    Unprocessable request or invalid data in token
    Permissions:
        This endpoint is accessable to only to Managers
    '''
    try:
        data = request.get_json()
        if 'title' not in data or 'recipe' not in data:
            abort(422)
        new_title = data['title']
        new_recipe = data['recipe']
        drink = Drink(title=new_title)
        drink.recipe = recipe if type(new_recipe) == \
            str else json.dumps(new_recipe)
        drink.insert()
        return jsonify({
            'success': True,
            'drinks': [drink.long()]
        })
    except Exception as e:
        print(e)
        abort(422)


@app.route('/drinks/<int:drink_id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def edit_drinks(jwt, drink_id):
    '''
    This endpoint is to edit an existing drink
    Parameters:
        drink_id: ID of the drink to be updated
        jwt: Decoded jwt token which may contain the title
             or the recipe of the drink to be updated
    Responses:
        200:    Updated drink in long form
        422:    Unprocessable request
    Permissions:
        This endpoint is accessable to only to Managers
    '''
    try:
        drink = Drink.query.get(drink_id)
        if drink:
            data = request.get_json()
            if 'title' in data:
                drink.title = data['title']
            if 'recipe' in data:
                drink.recipe = recipe if type(data['recipe']) == \
                               str else json.dumps(data['recipe'])
            drink.update()
        else:
            abort(404)
        return jsonify({
            'success': True,
            'drink': [drink.long()]
        })
    except Exception as e:
        print(e)
        abort(422)


@app.route('/drinks/<int:drink_id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(jwt, drink_id):
    '''
    This endpoint is to delete a drink
    Parameters:
        drink_id: ID of the drink to be deleted
    Responses:
        200:    ID of the deleted drink
        422:    Unprocessable request
    Permissions:
        This endpoint is accessble to only to Managers
    '''
    try:
        drink = Drink.query.filter(Drink.id == drink_id).one_or_none()
        if drink:
            drink.delete()
        else:
            abort(404)
        return jsonify({
            'success': True,
            'delete': drink_id
        })
    except Exception as e:
        print(e)
        abort(404)

# Error Handling


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
                    "success": False,
                    "error": 422,
                    "message": "unprocessable"
                    }), 422


@app.errorhandler(401)
def unprocessable(error):
    return jsonify({
                    "success": False,
                    "error": 401,
                    "message": "unauthorized"
                    }), 401


@app.errorhandler(404)
def not_found(error):
    return jsonify({
                    'success': False,
                    'error': 404,
                    'message': 'Resource not found'
                    }), 404


@app.errorhandler(AuthError)
def unauthorized(error):
    return jsonify({
                    'success': False,
                    'error': 401,
                    'message': 'Internal server error'
                    }), 401
