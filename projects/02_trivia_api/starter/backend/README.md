# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## Tasks

One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior. 

1. Use Flask-CORS to enable cross-domain requests and set response headers. 
2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories. 
3. Create an endpoint to handle GET requests for all available categories. 
4. Create an endpoint to DELETE question using a question ID. 
5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score. 
6. Create a POST endpoint to get questions based on category. 
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. 
8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 
9. Create error handlers for all expected errors including 400, 404, 422 and 500. 

REVIEW_COMMENT
```
This README is missing documentation of your endpoints. Below is an example for your endpoint to get all categories. Please use it as a reference for creating your documentation and resubmit your code. 
```

## Endpoints

##### GET /categories
* General
     * Returns a list of categories, success value and total number of categories
* Sample ```curl http://127.0.0.1:5000/categories```
```json
{
  "categories": {
    "1": "Art",
    "2": "Science",
    "3": "History",
    "4": "Geography",
    "5": "Entertainment",
    "6": "Sports"
  },
  "success": true,
  "total_categories": 6
}
```
##### GET /questions
* General
    * Returns a list of questions, success value, total number of questions, a list of categories and the current category. 
    * Results are paginated in groups of 10. Include a request argument to choose page number starting from 1
* Sample ```curl http://127.0.0.1:5000/questions```  or   ```curl http://127.0.0.1:5000/questions?page=1```

```json
{
  "categories": {
    "1": "Art",
    "2": "Science",
    "3": "History",
    "4": "Geography",
    "5": "Entertainment",
    "6": "Sports"
  },
  "current_category": null,
  "questions": [
    {
      "answer": "120 days",
      "category": "Science",
      "difficulty": 2,
      "id": 1,
      "question": "How long does a human red blood cell survive?"
    },
    {
      "answer": "Nectar",
      "category": "Science",
      "difficulty": 1,
      "id": 3,
      "question": "What do bees collect and use to create honey?"
    },
    {
      "answer": "AB negative",
      "category": "Science",
      "difficulty": 1,
      "id": 4,
      "question": "What is the rarest blood type?"
    },
    {
      "answer": "Leaf",
      "category": "Science",
      "difficulty": 1,
      "id": 5,
      "question": "What part of the plant conducts photosynthesis?"
    },
    {
      "answer": "Middle ear",
      "category": "Science",
      "difficulty": 2,
      "id": 6,
      "question": "Where can you find the smallest bone in the human body?"
    },
    {
      "answer": "3",
      "category": "Science",
      "difficulty": 2,
      "id": 7,
      "question": "How many hearts does an octopus have?"
    },
    {
      "answer": "California",
      "category": "Science",
      "difficulty": 3,
      "id": 8,
      "question": "The oldest living tree is 4,843 years old and can be found where?"
    },
    {
      "answer": "Sir Charles Wood",
      "category": "History",
      "difficulty": 1,
      "id": 13,
      "question": "Who introduced English as official language?"
    },
    {
      "answer": "S. Mukherjee",
      "category": "History",
      "difficulty": 1,
      "id": 12,
      "question": "Who was the first woman IAF chief?"
    },
    {
      "answer": "Santosh Yadav",
      "category": "History",
      "difficulty": 1,
      "id": 11,
      "question": "Who was the first woman to climb Mount Everest?"
    }
  ],
  "success": true,
  "total_questions": 21
}
```
##### GET /categories/{category_id}/questions
* General
    * Fetches the questions under the given category
    * Returns success value, list of questions paginated, total number of questions and the choosen category
* Sample ```curl http://127.0.0.1:5000/categories/4/questions```
```json
{
  "category": "Geography",
  "questions": [
    {
      "answer": "Russia",
      "category": "Geography",
      "difficulty": 2,
      "id": 18,
      "question": "Which country has largest land mass"
    }
  ],
  "success": true,
  "total_questions": 1
}
```

##### DELETE /questions/{question_id}
* General
    * Deletes the question with given question_id
    * Returns success value, deleted question id, refreshed questions with pagination and the total number of questions after deletion
* Sample ```curl -X DELETE http://127.0.0.1:5000/questions/14```
```json
{
  "deleted": 14,
  "questions": [
    {
      "answer": "120 days",
      "category": "Science",
      "difficulty": 2,
      "id": 1,
      "question": "How long does a human red blood cell survive?"
    },
    {
      "answer": "Nectar",
      "category": "Science",
      "difficulty": 1,
      "id": 3,
      "question": "What do bees collect and use to create honey?"
    },
    {
      "answer": "AB negative",
      "category": "Science",
      "difficulty": 1,
      "id": 4,
      "question": "What is the rarest blood type?"
    },
    {
      "answer": "Leaf",
      "category": "Science",
      "difficulty": 1,
      "id": 5,
      "question": "What part of the plant conducts photosynthesis?"
    },
    {
      "answer": "Middle ear",
      "category": "Science",
      "difficulty": 2,
      "id": 6,
      "question": "Where can you find the smallest bone in the human body?"
    },
    {
      "answer": "3",
      "category": "Science",
      "difficulty": 2,
      "id": 7,
      "question": "How many hearts does an octopus have?"
    },
    {
      "answer": "California",
      "category": "Science",
      "difficulty": 3,
      "id": 8,
      "question": "The oldest living tree is 4,843 years old and can be found where?"
    },
    {
      "answer": "Sir Charles Wood",
      "category": "History",
      "difficulty": 1,
      "id": 13,
      "question": "Who introduced English as official language?"
    },
    {
      "answer": "S. Mukherjee",
      "category": "History",
      "difficulty": 1,
      "id": 12,
      "question": "Who was the first woman IAF chief?"
    },
    {
      "answer": "Santosh Yadav",
      "category": "History",
      "difficulty": 1,
      "id": 11,
      "question": "Who was the first woman to climb Mount Everest?"
    }
  ],
  "success": true,
  "total_questions": 20
}
```
##### POST /questions
* General
    * Adds a question to the list if a question details is passes as data. It should have the question, answer, difficulty and the category
    * If a search term is provided returns a list of questions matching the given search term
    * Returns success value, paginated list of questions and the total number of questions.
* Sample 
```curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"question":"How many basketballs teams are in NBA?", "answer" : "30", "type":"Sports", "difficulty" : 2}'```
```curl -X POST http://127.0.0.1:5000/questions -H "Content-Type: application/json" -d '{"searchTerm":"woman"}'```
```json
{
  "questions": [
    {
      "answer": "S. Mukherjee",
      "category": "History",
      "difficulty": 1,
      "id": 12,
      "question": "Who was the first woman IAF chief?"
    },
    {
      "answer": "Santosh Yadav",
      "category": "History",
      "difficulty": 1,
      "id": 11,
      "question": "Who was the first woman to climb Mount Everest?"
    },
    {
      "answer": "Mother Teresa",
      "category": "History",
      "difficulty": 1,
      "id": 9,
      "question": "Who was the first woman to receive Nobel Price?"
    }
  ],
  "success": true,
  "total_questions": 3
}
```
##### POST /quizzes
* General
    * Fetches a random unplayed question from the picked category. Previously played question list and the quiz category must be given in json
    * Returns the question and success value
* Sample ```curl -X POST http://127.0.0.1:5000/quizzes -H "Content-Type: application/json" -d '{"previous_questions" : [5,6], "quiz_category" : {"type" : "Science", "id":2}}'```
```json
{
    'question' : {
        "answer": "Mother Teresa",
        "category": "History",
        "difficulty": 1,
        "id": 9,
        "question": "Who was the first woman to receive Nobel Price?"
    },
    'success' : true
    }
```

## Error Handling
Errors are handled in json format
```json
{
  "error": 400,
  "message": "Bad request",
  "success": false
}
```
The API will return three error types when the request fails
* 400 : Bad request
* 404 : Resource not found
* 422 : Unprocessable

## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```