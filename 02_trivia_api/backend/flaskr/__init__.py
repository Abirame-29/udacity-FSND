import os
import sys
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def paginate_questions(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
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
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-type, Authorization')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET, POST, PATCH, DELETE, OPTIONS')
        return response

    @app.route('/categories', methods=['GET'])
    def get_categories():
        categories = Category.query.all()
        formatted_categories = {}
        for category in categories:
            formatted_categories[category.id] = category.type
        if len(formatted_categories) == 0:
            abort(404)
        return jsonify({
            'success': True,
            'categories': formatted_categories,
            'total_categories': len(formatted_categories)
            })

    @app.route('/questions', methods=['GET'])
    def get_questions():
        try:
            questions = Question.query.all()
            current_questions = paginate_questions(request, questions)
            categories = Category.query.all()
            formatted_categories = {}
            for category in categories:
                formatted_categories[category.id] = category.type
            if len(current_questions) == 0:
                abort(404)
            return jsonify({
                'success': True,
                'categories': formatted_categories,
                'current_category': None,
                'questions': current_questions,
                'total_questions': Question.query.count()
                })
        except:
            print(sys.exc_info())
            abort(404)

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        ques = Question.query.filter(Question.id == question_id).one_or_none()
        if ques is None:
            abort(404)
        ques.delete()
        questions = Question.query.all()
        current_questions = paginate_questions(request, questions)
        return jsonify({
            'success': True,
            'deleted': question_id,
            'questions': current_questions,
            'total_questions': Question.query.count()
            })

    @app.route('/questions', methods=['POST'])
    def add_question():
        try:
            data = request.get_json()
            search = data.get('searchTerm', None)
            if search:
                questions = Question.query.\
                            filter(Question.question.ilike("%"+search+"%"))\
                            .all()
                current_questions = paginate_questions(request, questions)
                return jsonify({
                    'success': True,
                    'questions': current_questions,
                    'total_questions': len(questions)
                    })
            else:
                category = Category.query.get(data.get('category'))
                question = Question(
                    question=data.get('question', None),
                    answer=data.get('answer', None),
                    difficulty=data.get('difficulty', None),
                    category=category.id
                )
                if question.question is None or question.answer is None or \
                   question.category is None or question.difficulty is None:
                    abort(400)
                question.insert()
                questions = Question.query.all()
                current_questions = paginate_questions(request, questions)
                return jsonify({
                    'success': True,
                    'created': question.id,
                    'questions': current_questions,
                    'total_questions': Question.query.count()
                })
        except:
            print(sys.exc_info())
            abort(404)

    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def get_category_questions(category_id):
        try:
            category_id = str(category_id)
            category = Category.query.get(category_id)
            if category is None:
                abort(404)
            ques = Question.query.filter(Question.category == category_id)
            current_questions = paginate_questions(request, ques.all())
            return jsonify({
                'success': True,
                'questions': current_questions,
                'total_questions': ques.count(),
                'category': category.type
                })
        except:
            print(sys.exc_info())
            abort(404)

    @app.route('/quizzes', methods=['POST'])
    def get_next_question():
        data = request.get_json()
        if data is None:
            abort(400)
        previous_questions = data['previous_questions']
        if data['quiz_category']['id'] == 0:
            questions = Question.query.all()
        else:
            category = str(data['quiz_category']['id'])
            questions = Question.query.filter(Question.category == category)\
                        .all()

        question_ids = [question.id for question in questions]

        for prev in previous_questions:
            question_ids.remove(prev)

        if len(question_ids) == 0:
            return jsonify({
                'success': True,
                'question': None
                })
        random_index = random.randrange(len(question_ids))
        random_id = question_ids[random_index]
        random_question = Question.query.get(random_id)
        if random_question is None:
            abort(404)
        return jsonify({
            'success': True,
            'question': random_question.format()
            })

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'Bad request'
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'Resource not found'
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'Unprocessable'
        }), 422

    @app.errorhandler(500)
    def unprocessable(error):
        return jsonify({
            'success': False,
            'error': 500,
            'message': 'Internal server error'
        }), 500

    return app
