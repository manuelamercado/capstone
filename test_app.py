import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from database.models import setup_db, Actor, Movie
from auth.auth import AuthError, requires_auth

CASTING_ASSISTANT = os.getenv('CASTING_ASSISTANT')
CASTING_DIRECTOR = os.getenv('CASTING_DIRECTOR')
EXECUTIVE_PRODUCER = os.getenv('EXECUTIVE_PRODUCER')

class CasptoneTestCase(unittest.TestCase):
  """This class represents the Capstone test case"""

  def setUp(self):
    """Define test variables and initialize app."""
    self.app = create_app()
    self.client = self.app.test_client
    self.database_name = "casptone_test"
    setup_db(self.app)

    self.new_actor = {
      "name": "Manuela Mercado",
      "age": 25,
      "gender": "F",
      "movies": [1, 2]
    }

    self.new_movie = {
      "title": "Manuela Mercado",
      "release_year": "Fri, 15 May 2020 00:00:00 GMT",
      "actors": [1, 2]
    }

    # binds the app to the current context
    with self.app.app_context():
      self.db = SQLAlchemy()
      self.db.init_app(self.app)
      # create all tables
      self.db.create_all()
    
  def tearDown(self):
    """Executed after reach test"""
    pass

  """
  Tests for successful operation and for expected errors.
  """
  def test_get_actors_casting_assistant(self):
    res = self.client().get('/actors',
      headers={
        'Authorization': 'Bearer {}'.format(CASTING_ASSISTANT)
      })
    data = json.loads(res.data)

    self.assertEqual(res.status_code, 200)
    self.assertEqual(data['success'], True)
    self.assertTrue(len(data['actors']))

  def test_get_movies_casting_director(self):
    res = self.client().get('/movies',
      headers={
        'Authorization': 'Bearer {}'.format(CASTING_DIRECTOR)
      })
    data = json.loads(res.data)

    self.assertEqual(res.status_code, 200)
    self.assertEqual(data['success'], True)
    self.assertTrue(len(data['movies']))

  def test_404_get_actors_without_auth(self):
    res = self.client().get('/authors')
    data = json.loads(res.data)

    self.assertEqual(res.status_code, 404)
    self.assertEqual(data['success'], False)
    self.assertEqual(data['message'], 'Not found')

  def test_create_new_actor_casting_director(self):
    res = self.client().post('/actors',
      headers={
        'Authorization': 'Bearer {}'.format(CASTING_DIRECTOR)
      },
      json=self.new_actor
    )
    data = json.loads(res.data)

    self.assertEqual(res.status_code, 200)
    self.assertEqual(data['success'], True)
    self.assertTrue(len(data['actors']))

  def test_401_create_new_actor_casting_assistant(self):
    res = self.client().post('/actors',
      headers={
        'Authorization': 'Bearer {}'.format(CASTING_ASSISTANT)
      },
      json=self.new_actor
    )
    data = json.loads(res.data)

    self.assertEqual(res.status_code, 401)
    self.assertEqual(data['success'], False)
    self.assertEqual(data['message'], 'Permissions not found.')

  def test_create_new_movie_executive_producer(self):
    res = self.client().post('/movies',
      headers={
        'Authorization': 'Bearer {}'.format(EXECUTIVE_PRODUCER)
      },
      json=self.new_movie
    )
    data = json.loads(res.data)

    self.assertEqual(res.status_code, 200)
    self.assertEqual(data['success'], True)
    self.assertTrue(len(data['movies']))

  def test_401_create_new_movie_casting_assistant(self):
    res = self.client().post('/movies',
      headers={
        'Authorization': 'Bearer {}'.format(CASTING_ASSISTANT)
      },
      json=self.new_movie
    )
    data = json.loads(res.data)

    self.assertEqual(res.status_code, 401)
    self.assertEqual(data['success'], False)
    self.assertEqual(data['message'], 'Permissions not found.')

  def test_update_actor_casting_director(self):
    res = self.client().patch('/actors/3',
      headers={
        'Authorization': 'Bearer {}'.format(CASTING_DIRECTOR)
      },
      json={'age': 10}
    )
    data = json.loads(res.data)
    actor = Actor.query.filter(Actor.id == 3).one_or_none()

    self.assertEqual(res.status_code, 200)
    self.assertEqual(data['success'], True)
    self.assertEqual(actor.format()['age'], 10)

  def test_400_update_actor_executive_producer_with_unexistent_actor(self):
    res = self.client().patch('/actors/100000',
      headers={
        'Authorization': 'Bearer {}'.format(EXECUTIVE_PRODUCER)
      },
      json={'age': 10}
    )
    data = json.loads(res.data)

    self.assertEqual(res.status_code, 400)
    self.assertEqual(data['success'], False)
    self.assertEqual(data['message'], 'Bad request')

  def test_update_movie_casting_director(self):
    res = self.client().patch('/movies/2',
      headers={
        'Authorization': 'Bearer {}'.format(CASTING_DIRECTOR)
      },
      json={'title': '10 hours'}
    )
    data = json.loads(res.data)
    movie = Movie.query.filter(Movie.id == 2).one_or_none()

    self.assertEqual(res.status_code, 200)
    self.assertEqual(data['success'], True)
    self.assertEqual(movie.format()['title'], '10 hours')

  def test_401_update_movie_casting_assistant(self):
    res = self.client().patch('/movies/3',
      headers={
        'Authorization': 'Bearer {}'.format(CASTING_ASSISTANT)
      },
      json={}
    )
    data = json.loads(res.data)

    self.assertEqual(res.status_code, 401)
    self.assertEqual(data['success'], False)
    self.assertEqual(data['message'], 'Permissions not found.')

  def test_delete_actor_casting_director(self):
    res = self.client().delete('/actors/2',
      headers={
        'Authorization': 'Bearer {}'.format(CASTING_DIRECTOR)
      }
    )
    data = json.loads(res.data)

    actor = Actor.query.filter(Actor.id == 2).one_or_none()

    self.assertEqual(res.status_code, 200)
    self.assertEqual(data['success'], True)
    self.assertEqual(data['delete'], 2)
    self.assertEqual(actor, None)

  def test_422_if_actor_does_not_exist_executive_producer(self):
    res = self.client().delete('/actors/2999',
    headers={
        'Authorization': 'Bearer {}'.format(EXECUTIVE_PRODUCER)
      }
    )
    data = json.loads(res.data)

    self.assertEqual(res.status_code, 422)
    self.assertEqual(data['success'], False)
    self.assertEqual(data['message'], 'Unprocessable')

  def test_delete_movie_executive_producer(self):
    res = self.client().delete('/movies/3',
      headers={
        'Authorization': 'Bearer {}'.format(EXECUTIVE_PRODUCER)
      }
    )
    data = json.loads(res.data)

    movie = Movie.query.filter(Movie.id == 3).one_or_none()

    self.assertEqual(res.status_code, 200)
    self.assertEqual(data['success'], True)
    self.assertEqual(data['delete'], 3)
    self.assertEqual(movie, None)

  def test_422_if_movie_does_not_exist_executive_producer(self):
    res = self.client().delete('/movies/3000',
    headers={
        'Authorization': 'Bearer {}'.format(EXECUTIVE_PRODUCER)
      }
    )
    data = json.loads(res.data)

    self.assertEqual(res.status_code, 422)
    self.assertEqual(data['success'], False)
    self.assertEqual(data['message'], 'Unprocessable')

  def test_405_if_actor_creation_not_allowed_executive_producer(self):
    res = self.client().post('/actors/45',
      headers={
        'Authorization': 'Bearer {}'.format(EXECUTIVE_PRODUCER)
      },
      json=self.new_actor
    )
    data = json.loads(res.data)

    self.assertEqual(res.status_code, 405)
    self.assertEqual(data['success'], False)
    self.assertEqual(data['message'], 'Method not allowed')

# Make the tests conveniently executable
if __name__ == "__main__":
  unittest.main()
