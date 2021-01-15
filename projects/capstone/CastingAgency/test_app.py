
import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import setup_db, Movie, Actor
import os

database_path = os.environ['DATABASE_URL']
CASTING_ASSISTANT = os.environ['CASTING_ASSISTANT_JWT']
CASTING_DIRECTOR = os.environ['CASTING_DIRECTOR_JWT']
EXECUTIVE_PRODUCER = os.environ['EXECUTIVE_PRODUCER_JWT']


def get_headers(token):
    return {'Authorization': f'Bearer {token}'}


class CastingAgencyTestCase(unittest.TestCase):
    def setUp(self):
        # Define test variables and initialize app.
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "test_agency"
        self.database_path = database_path
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        # Executed after reach test
        pass

    def test_get_paginated_actors_casting_assistant(self):
        res = self.client().get('/actors',
                                headers=get_headers(CASTING_ASSISTANT))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_actors'])
        self.assertTrue(data['actors'])

    def test_get_paginated_actors_casting_director(self):
        res = self.client().get('/actors',
                                headers=get_headers(CASTING_DIRECTOR))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_actors'])
        self.assertTrue(data['actors'])

    def test_get_paginated_actors_executive_producer(self):
        res = self.client().get('/actors',
                                headers=get_headers(EXECUTIVE_PRODUCER))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_actors'])
        self.assertTrue(data['actors'])

    def test_get_paginated_actors_invalid_page(self):
        res = self.client().get('/actors?page=500',
                                headers=get_headers(CASTING_ASSISTANT))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable')

    def test_get_paginated_movies_casting_assistant(self):
        res = self.client().get('/movies',
                                headers=get_headers(CASTING_ASSISTANT))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_movies'])
        self.assertTrue(data['movies'])

    def test_get_paginated_movies_casting_director(self):
        res = self.client().get('/movies',
                                headers=get_headers(CASTING_DIRECTOR))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_movies'])
        self.assertTrue(data['movies'])

    def test_get_paginated_movies_executive_producer(self):
        res = self.client().get('/movies',
                                headers=get_headers(EXECUTIVE_PRODUCER))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_movies'])
        self.assertTrue(data['movies'])

    def test_get_paginated_movies_invalid_page(self):
        res = self.client().get('/movies?page=500',
                                headers=get_headers(CASTING_ASSISTANT))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable')

    def test_post_actor_casting_assistant(self):
        res = self.client().post(
            '/actors',
            json={
                'name': 'Jane William',
                'age': 41,
                'gender': 'Female'},
            headers=get_headers(CASTING_ASSISTANT))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unauthorized')

    def test_post_actor_without_data(self):
        res = self.client().post('/actors',
                                 headers=get_headers(CASTING_DIRECTOR))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable')

    def test_post_actor_invalid_method(self):
        res = self.client().post(
            '/actors/200',
            json={
                'name': 'Jane William',
                'age': 41,
                'gender': 'Female'},
            headers=get_headers(CASTING_DIRECTOR))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Method not allowed')

    def test_post_actor_casting_director(self):
        res = self.client().post(
            '/actors',
            json={
                'name': 'Jane William',
                'age': 41,
                'gender': 'Female'},
            headers=get_headers(CASTING_DIRECTOR))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_actors'])
        self.assertTrue(data['actors'])
        self.assertTrue(data['created_actor_id'])

    def test_post_actor_executive_producer(self):
        res = self.client().post(
            '/actors',
            json={
                'name': 'Mary Jane',
                'age': 37,
                'gender': 'Female'},
            headers=get_headers(EXECUTIVE_PRODUCER))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_actors'])
        self.assertTrue(data['actors'])
        self.assertTrue(data['created_actor_id'])

    def test_post_movie_casting_assistant(self):
        res = self.client().post(
            '/movies',
            json={
                'title': 'Despicable me',
                'release_date': '2021-02-05'},
            headers=get_headers(CASTING_ASSISTANT))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unauthorized')

    def test_post_movie_without_data(self):
        res = self.client().post('/movies',
                                 headers=get_headers(EXECUTIVE_PRODUCER))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable')

    def test_post_movie_invalid_method(self):
        res = self.client().post(
            '/movies/200',
            json={
                'title': 'Despicable me',
                'release_date': '2021-02-05'},
            headers=get_headers(EXECUTIVE_PRODUCER))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Method not allowed')

    def test_post_movie_casting_director(self):
        res = self.client().post(
            '/movies',
            json={
                'title': 'Despicable me',
                'release_date': '2021-02-05'},
            headers=get_headers(CASTING_DIRECTOR))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unauthorized')

    def test_post_movie_executive_producer(self):
        res = self.client().post(
            '/movies',
            json={
                'title': 'Despicable me4',
                'release_date': '2021-02-05'},
            headers=get_headers(EXECUTIVE_PRODUCER))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_movies'])
        self.assertTrue(data['movies'])
        self.assertTrue(data['created_movie_id'])

    def test_edit_actor_invalid_actor(self):
        res = self.client().patch(
            '/actors/500',
            json={
                'age': 50},
            headers=get_headers(CASTING_DIRECTOR))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable')

    def test_edit_actor_casting_assistant(self):
        res = self.client().patch(
            '/actors/1',
            json={
                'age': 50},
            headers=get_headers(CASTING_ASSISTANT))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unauthorized')

    def test_edit_actor_casting_director(self):
        res = self.client().patch(
            '/actors/1',
            json={
                'age': 50},
            headers=get_headers(CASTING_DIRECTOR))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_actors'])
        self.assertTrue(data['actors'])
        self.assertTrue(data['edited_actor_id'])

    def test_edit_actor_executive_producer(self):
        res = self.client().patch(
            '/actors/1',
            json={
                'age': 47},
            headers=get_headers(EXECUTIVE_PRODUCER))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_actors'])
        self.assertTrue(data['actors'])
        self.assertTrue(data['edited_actor_id'])

    def test_edit_movie_invalid_movie(self):
        res = self.client().patch(
            '/movies/500',
            json={
                'release_date': '2021-12-12'},
            headers=get_headers(CASTING_DIRECTOR))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable')

    def test_edit_movie_casting_assistant(self):
        res = self.client().patch(
            '/movies/1',
            json={
                'release_date': '2021-12-12'},
            headers=get_headers(CASTING_ASSISTANT))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unauthorized')

    def test_edit_movie_casting_director(self):
        res = self.client().patch(
            '/movies/1',
            json={
                'release_date': '2021-12-12'},
            headers=get_headers(CASTING_DIRECTOR))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_movies'])
        self.assertTrue(data['movies'])
        self.assertTrue(data['edited_movie_id'])

    def test_edit_movie_executive_producer(self):
        res = self.client().patch(
            '/movies/1',
            json={
                'release_date': '2021-12-12'},
            headers=get_headers(EXECUTIVE_PRODUCER))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_movies'])
        self.assertTrue(data['movies'])
        self.assertTrue(data['edited_movie_id'])

    def delete_actor_invalid_actor(self):
        res = self.client().delete('/actors/342',
                                   headers=get_headers(CASTING_DIRECTOR))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable')

    def delete_actor_casting_assistant(self):
        res = self.client().delete('/actors/1',
                                   headers=get_headers(CASTING_ASSISTANT))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unauthorized')

    def delete_actor_casting_director(self):
        res = self.client().delete('/actors/1',
                                   headers=get_headers(CASTING_DIRECTOR))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_actors'])
        self.assertTrue(data['actors'])
        self.assertTrue(data['deleted_actor_id'])

    def delete_actor_executive_producer(self):
        res = self.client().delete('/actors/2',
                                   headers=get_headers(EXECUTIVE_PRODUCER))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_actors'])
        self.assertTrue(data['actors'])
        self.assertTrue(data['deleted_actor_id'])

    def delete_movie_invalid_movie(self):
        res = self.client().delete('/movies/342',
                                   headers=get_headers(CASTING_DIRECTOR))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable')

    def delete_movie_casting_assistant(self):
        res = self.client().delete('/movies/1',
                                   headers=get_headers(CASTING_ASSISTANT))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unauthorized')

    def delete_movie_casting_director(self):
        res = self.client().delete('/movies/1',
                                   headers=get_headers(CASTING_DIRECTOR))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unauthorized')

    def delete_movie_executive_producer(self):
        res = self.client().delete('/movies/1',
                                   headers=get_headers(EXECUTIVE_PRODUCER))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_movies'])
        self.assertTrue(data['movies'])
        self.assertTrue(data['deleted_movie_id'])


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
