import os
import sys
import json
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, setup_db, Actor, Movie
from auth import AuthError, requires_auth

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  migrate = Migrate(app, db)
  CORS(app)

  # CORS Headers
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

  ## ROUTES
  @app.route('/')
  def index():
    return 'This is the default index of Casting Agency Api Project.'

  '''
  GET /actors
    it should be an endpoint accesible for all roles
    it should require the 'get:actors' permission
  returns status code 200 and json {'success': True, 'actors': actors} where actors is the list of actors
    or appropriate status code indicating reason for failure
  '''
  @app.route('/actors', methods=['GET'])
  @requires_auth('get:actors')
  def retrieve_all_actors(jwt):
    if jwt:
      actors_data = Actor.query.order_by(Actor.id).all()
      actors = [actor.format() for actor in actors_data]

      if len(actors_data):
        return jsonify({
          'success': True,
          'actors': actors
        })
      else:
        abort(404)
    else:
      abort(401)

  '''
  GET /movies
    it should be an endpoint accesible for all roles
    it should require the 'get:movies' permission
  returns status code 200 and json {'success': True, 'movies': movies} where movies is the list of movies
    or appropriate status code indicating reason for failure
  '''
  @app.route('/movies', methods=['GET'])
  @requires_auth('get:movies')
  def retrieve_all_movies(jwt):
    if jwt:
      movies_data = Movie.query.order_by(Movie.id).all()
      movies = [movie.format() for movie in movies_data]

      if len(movies_data):
        return jsonify({
          'success': True,
          'movies': movies
        })
      else:
        abort(404)
    else:
      abort(401)

  '''
  POST /actors
    it should create a new row in the actors table
    it should require the 'post:actors' permission
  returns status code 200 and json {'success': True, 'actors': actor} where actor is an array containing only the newly created actor
    or appropriate status code indicating reason for failure
  '''
  @app.route('/actors', methods=['POST'])
  @requires_auth('post:actors')
  def add_actor(jwt):
    if jwt:
      body = request.get_json()

      new_name = body.get('name', None)
      new_age = body.get('age', None)
      new_gender = body.get('gender', None)
      new_movies = body.get('movies', None)

      try:
        actor = Actor(name=new_name, age=new_age, gender=new_gender)
        movies = Movie.query.filter(Movie.id.in_(new_movies)).order_by(Movie.id).all()

        if len(movies):
          for movie in movies:
            actor.movies.append(Movie.query.get(movie))

        actor.insert()

        return jsonify({
          'success': True,
          'actors': [actor.format()],
        })

      except:
        print(sys.exc_info())
        abort(422)
    else:
      abort(401)

  '''
  POST /movies
    it should create a new row in the movies table
    it should require the 'post:movies' permission
  returns status code 200 and json {'success': True, 'movies': movie} where movie is an array containing only the newly created movie
    or appropriate status code indicating reason for failure
  '''
  @app.route('/movies', methods=['POST'])
  @requires_auth('post:movies')
  def add_movie(jwt):
    if jwt:
      body = request.get_json()

      new_title = body.get('title', None)
      new_release_year = body.get('release_year', None)
      new_actors = body.get('actors', None)

      try:
        movie = Movie(title=new_title, release_year=new_release_year)
        actors = Actor.query.filter(Actor.id.in_(new_actors)).order_by(Actor.id).all()

        if len(actors):
          for actor in actors:
            movie.actors.append(actor)

        movie.insert()

        return jsonify({
          'success': True,
          'movies': [movie.format()],
        })

      except:
        print(sys.exc_info())
        abort(422)
    else:
      abort(401)

  '''
  PATCH /actors/<id>
    where <id> is the existing model id
    it should respond with a 404 error if <id> is not found
    it should update the corresponding row for <id>
    it should require the 'patch:actors' permission
  returns status code 200 and json {'success': True, 'actors': actor} where actor is an array containing only the updated actor
    or appropriate status code indicating reason for failure
  '''
  @app.route('/actors/<int:actor_id>', methods=['PATCH'])
  @requires_auth('patch:actors')
  def update_actor(jwt, actor_id):
    if jwt:
      body = request.get_json()

      try:
        actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
        if actor is None:
          abort(404)

        if 'name' in body:
          actor.name = body.get('name', None)
        
        if 'age' in body:
          actor.age = body.get('age', None)

        if 'gender' in body:
          actor.gender = body.get('gender', None)

        if 'movies' in body:
          new_movies = body.get('movies', None)
          movies = Movie.query.filter(Movie.id.in_(new_movies)).order_by(Movie.id).all()

          for movie in movies:
            actor.movies.append(movie)
        
        actor.update()

        return jsonify({
          'success': True,
          'actors': [actor.format()]
        })

      except:
        print(sys.exc_info())
        abort(400)
    else:
      abort(401)

  '''
    PATCH /movies/<id>
      where <id> is the existing model id
      it should respond with a 404 error if <id> is not found
      it should update the corresponding row for <id>
      it should require the 'patch:movies' permission
    returns status code 200 and json {'success': True, 'movies': movie} where movie is an array containing only the updated movie
      or appropriate status code indicating reason for failure
  '''
  @app.route('/movies/<int:movie_id>', methods=['PATCH'])
  @requires_auth('patch:movies')
  def update_movie(jwt, movie_id):
    if jwt:
      body = request.get_json()

      try:
        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
        if movie is None:
          abort(404)

        if 'title' in body:
          movie.title = body.get('title', None)
        
        if 'release_year' in body:
          movie.release_year = body.get('release_year', None)

        if 'actors' in body:
          new_actors = body.get('actors', None)
          actors = Actor.query.filter(Actor.id.in_(new_actors)).order_by(Actor.id).all()

          for actor in actors:
            movie.actors.append(actor)
        
        movie.update()

        return jsonify({
          'success': True,
          'movies': [movie.format()]
        })

      except:
        print(sys.exc_info())
        abort(400)
    else:
      abort(401)

  '''
  DELETE /actors/<id>
    where <id> is the existing model id
    it should respond with a 404 error if <id> is not found
    it should delete the corresponding row for <id>
    it should require the 'delete:actors' permission
  returns status code 200 and json {'success': True, 'delete': id} where id is the id of the deleted record
    or appropriate status code indicating reason for failure
  '''
  @app.route('/actors/<int:actor_id>', methods=['DELETE'])
  @requires_auth('delete:actors')
  def delete_actor(jwt, actor_id):
    if jwt:
      try:
        actor = Actor.query.filter(Actor.id == actor_id).one_or_none()

        if actor is None:
          abort(404)

        actor.delete()

        return jsonify({
          'success': True,
          'delete': actor.id
        })

      except:
        abort(422)
    else:
      abort(401)

  '''
  DELETE /movies/<id>
    where <id> is the existing model id
    it should respond with a 404 error if <id> is not found
    it should delete the corresponding row for <id>
    it should require the 'delete:movies' permission
  returns status code 200 and json {'success': True, 'delete': id} where id is the id of the deleted record
    or appropriate status code indicating reason for failure
  '''
  @app.route('/movies/<int:movie_id>', methods=['DELETE'])
  @requires_auth('delete:movies')
  def delete_movie(jwt, movie_id):
    if jwt:
      try:
        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()

        if movie is None:
          abort(404)

        movie.delete()

        return jsonify({
          'success': True,
          'delete': movie.id
        })

      except:
        abort(422)
    else:
      abort(401)

  ## Error Handling
  '''
  Error handling for unprocessable entity
  '''
  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
      'success': False, 
      'error': 422,
      'message': 'Unprocessable'
      }), 422

  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
      'success': False, 
      'error': 400,
      'message': 'Bad request'
      }), 400
  '''
  Error handler for 404
  '''
  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      'success': False, 
      'error': 404,
      'message': 'Not found'
      }), 404

  '''
  Error handler for AuthError
  '''
  @app.errorhandler(AuthError)
  def authorization_error(error):
    return jsonify({
      'success': False,
      'error': error.status_code,
      'message': error.error['description']
      }), 401

  @app.errorhandler(401)
  def not_authorized(error):
    return jsonify({
      'success': False, 
      'error': 401,
      'message': 'Not authorized'
      }), 401

  @app.errorhandler(403)
  def not_found_permission(error):
    return jsonify({
      'success': False, 
      'error': 403,
      'message': 'Do not have permissions'
      }), 403

  @app.errorhandler(405)
  def method_not_allowed(error):
    return jsonify({
      'success': False, 
      'error': 405,
      'message': 'Method not allowed'
      }), 405

  @app.errorhandler(500)
  def server_error(error):
    return jsonify({
      'success': False, 
      'error': 500,
      'message': 'Server error'
      }), 500

  return app

APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=5000, debug=True)