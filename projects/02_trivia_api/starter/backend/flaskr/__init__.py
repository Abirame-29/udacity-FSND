import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginate_questions(request, selection):
  page = request.args.get('page', 1, type=int)
  start =  (page - 1) * QUESTIONS_PER_PAGE
  end = start + QUESTIONS_PER_PAGE

  questions = [question.format() for question in selection]
  current_questions = questions[start:end]

  return current_questions


def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  CORS(app)
  
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-type, Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')
    return response

  @app.route('/categories', methods = ['GET'])
  def get_categories():
    categories = Category.query.all()
    formatted_categories = [category.format() for category in categories]
    if len(formatted_categories)==0:
      abort(404)
    return jsonify({
      'success' : True,
      'categories' : formatted_categories,
      'total_categories' : len(formatted_categories)
    })

  @app.route('/questions', methods = ['GET'])
  def get_questions():
    questions = Question.query.all()
    current_questions = paginate_questions(request, questions)
    categories = Category.query.all()
    formatted_categories = [category.format() for category in categories]
    if len(current_questions)==0:
      abort(404)
    return jsonify({
      'success' : True,
      'categories' : formatted_categories,
      'current_category' : None,
      'questions' : current_questions,
      'total_questions' : Question.query.count()
    })

  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):
    question = Question.query.filter(Question.id==question_id).one_or_none()
    if question is None:
      abort(404)
    question.delete()
    questions = Question.query.all()
    current_questions = paginate_questions(request, questions)
    return jsonify({
      'success' : True,
      'deleted' : question_id,
      'questions' : current_questions,
      'total_questions' : Question.query.count()
    })

  @app.route('/questions', methods=['POST'])
  def add_question():
    try:
      data = request.get_json()
      search = data.get('search',None)
      if search:
        questions = Question.query.filter(Question.question.ilike("%"+search+"%")).all()
        current_questions = paginate_questions(request,questions)
        return jsonify({
          'success' : True,
          'questions' : current_questions,
          'total_questions' : len(questions)
        })
      else:
        question = Question(
          question = data.get('question',None),
          answer = data.get('answer',None),
          difficulty = data.get('difficulty',None),
          category = data.get('category',None)
        )
        question.insert()
        questions = Question.query.all()
        current_questions = paginate_questions(request, questions)
        return jsonify({
          'success' : True,
          'created' : question.id,
          'questions' : current_questions,
          'total_questions' : Question.query.count()
        })
    except:
      abort(422)


  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''

  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''


  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''

  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      'success' : False,
      'error' : 404,
      'message' : 'Resource not found'
    })

  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
      'success' : False,
      'error' : 422,
      'message' : 'Unprocessable'
    })
  
  return app

    