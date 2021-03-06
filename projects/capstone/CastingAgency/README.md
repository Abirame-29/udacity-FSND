# Capstone Project - Casting Agency

This is the capstone project for the Udacity Full Stack Nanodegree program. 
The Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies. The agency includes a casting assistant, casting director and an executive producer who all have different roles / permissions in the agency. The Authorization and Access management of users is implemented using `auth0`.

### URLs

Casting Agency URL: https://my-casting-agency-app.herokuapp.com/ 
Heroku GitHub repository: https://git.heroku.com/my-casting-agency-app.git 

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

I recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once the virtual environment is setup and running, install dependencies by navigating to the working project directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM used to handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension used to handle cross origin requests. 

- [jose](https://python-jose.readthedocs.io/en/latest/) JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS.

## Running the server

From within the directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=app.py
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to application `app.py`. 

## Authentication

### Casting Assistant
A casting assistant is the lowest level of authority and is only permitted to view actors and movies.

#### Permissions:
```bash
get:actors | get:movies
```
#### Login details:
```bash
email: assistant@castingagency.com
password: Assistant#123
```

### Casting Director
A casting director mid-level authority and is permitted to view actors and movies as well as deleting an actor or adding an actor in the database and lastly, modifying actors and movies.

#### Permissions:
```bash
get:actors    | get:movies 
delete:actors | post:actors
patch:actors  | patch:movies
```
#### Login details:
```bash
email: director@castingagency.com
password: Director#123
```

### Executive Producer
The executive producer is the highest level of authority and is permitted to do any of the actions across the application.

#### Permissions:
```bash
get:actors    | get:movies 
delete:actors | delete:movies 
post:actors   | post:movies
patch:actors  | patch:movies
```
#### Login details:
```bash
email: producer@castingagency.com
password: Producer#123
```

## Endpoints

GET '/actors'
- First checks that the token provided is allowed to perform this operation. If authorized, then fetches a dictionary of actors.
- Header: Authorization Bearer token
- Request Arguments: token
- Returns: Each object in the actors dictionary and an object showing the total number of actors. 
```bash
{
    "actors": [
        {
            "age": 50,
            "gender": "Female",
            "id": 1,
            "name": "Jane William"
        },
        {
            "age": 37,
            "gender": "Female",
            "id": 2,
            "name": "Mary Jane"
        }
    ],
    "success": true,
    "total_actors": 2
}
```

GET '/movies'
- First checks that the token provided is allowed to perform this operation. If authorized, then fetches a dictionary of movies.
- Header: Authorization Bearer token
- Request Arguments: token
- Returns: Each object in the movies dictionary and an object showing the total number of movies. 
```bash
{
    "movies": [
        {
            "id": 1,
            "release_date": "Mon, 01 Mar 2021 00:00:00 GMT",
            "title": "Story of  Music"
        },
        {
            "id": 2,
            "release_date": "Wed, 15 Jun 2020 00:00:00 GMT",
            "title": "Despicable me"
        }
    ],
    "success": true,
    "total_movies": 2
}
```

POST '/actors'
- First checks that the token provided is allowed to perform this operation. If authorized, then takes in an object with key value pairs for the new actor namely the name, age and gender. 
- Header: Authorization Bearer token, Content-type: application/json
- Request Arguments: token
- Returns: An object containing the newly created actors's id, each object in the list of modified actors and an object showing the total number of actors.
```bash
{
    "actors": [
        {
            "age": 37,
            "gender": "Female",
            "id": 2,
            "name": "Mary Jane"
        }
    ],
    "created_actor_id": 2,
    "success": true,
    "total_actors": 2
}
```

POST '/movies'
- First checks that the token provided is allowed to perform this operation. If authorized, then takes in an object with key value pairs for the new movie namely the title and release_date. 
- Header: Authorization Bearer token, Content-type: application/json
- Request Arguments: token
- Returns: An object containing the newly created movie's id, each object in the list of modified movies and an object showing the total number of movies.
```bash
{
    "created_movie_id": 2,
    "movies": [
        {
            "id": 2,
            "release_date": "Wed, 15 Jun 2020 00:00:00 GMT",
            "title": "Despicable me"
        }
    ],
    "success": true,
    "total_movies": 2
}
```

PATCH '/actors'
- First checks that the token provided is allowed to perform this operation. If authorized, then takes in an object with key value pairs for the desired fields to be changes. 
- Header: Authorization Bearer token, Content-type: application/json
- Request Arguments: token, actor_id
- Returns: An object containing the updated actor.
```bash
{
    "actor": {
        "age": 35,
        "gender": "Female",
        "id": 2,
        "name": "Mary Jane"
    },
    "edited_actor_id": 2,
    "success": true
}
```

PATCH '/movies'
- First checks that the token provided is allowed to perform this operation. If authorized, then takes in an object with key value pairs for the desired fields to be changes. 
- Header: Authorization Bearer token, Content-type: application/json
- Request Arguments: token, movie_id
- Returns: An object containing the updated movie.
```bash
{
    "movie": {
        "id": 2,
        "release_date": "Wed, 15 Jun 2020 00:00:00 GMT",
        "title": "Despicable me 2"
    },
    "edited_movie_id": 2
    "success": true
}
```

DELETE '/actors/<int:actor_id>'
- First checks that the token provided is allowed to perform this operation. If authorized, then takes in a actor ID, if the actor exists, then it is deleted from the database
- Header: Authorization Bearer token
- Request Arguments: token, actor_id 
- Returns: The ID of the deleted actor and each object in the list of modified actors and an object showing the total number of actors.
```bash
{
    "actors": [],
    "deleted_actor_id": 1,
    "success": true,
    "total_actors": 0
}
```

DELETE '/movies/<int:movie_id>'
- First checks that the token provided is allowed to perform this operation. If authorized, then takes in a movie ID, if the movie exists, then it is deleted from the database
- Header: Authorization Bearer token
- Request Arguments: token, movie_id 
- Returns: The ID of the deleted movie and each object in the list of modified movies and an object showing the total number of movies.
```bash
{
    "deleted_movie_id": 1,
    "movies": [],
    "success": true,
    "total_movies": 0
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
* 500 : Internal server error
* 401 : Authorization error

## Testing
To run the tests, run
```
dropdb test_agency
createdb test_agency
psql test_agency < casting_agency.psql
python test_app.py
```
