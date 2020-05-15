import os
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, create_engine
from flask_sqlalchemy import SQLAlchemy
import json

# database_name = "capstone"
# database_path = "postgresql://{}/{}".format(os.environ['DATABASE_URL'], database_name)

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app):
  # app.config["SQLALCHEMY_DATABASE_URI"] = database_path
  app.config.from_object('config')
  db.app = app
  db.init_app(app)
  db.create_all()

'''
Movies and Actors table relationship
'''
movies = db.Table('movies',
  db.Column('movie_id', Integer, ForeignKey('Movie.id'), primary_key=True),
  db.Column('actor_id', Integer, ForeignKey('Actor.id'), primary_key=True)
)

'''
Actor
Entity for persons that acts in movies
'''
class Actor(db.Model):  
  __tablename__ = 'Actor'

  id = Column(Integer, primary_key=True)
  name = Column(String, nullable=False)
  age = Column(Integer, nullable=False)
  gender = Column(String, nullable=False)
  movies = db.relationship('Movie', secondary=movies, backref=db.backref('actors'), lazy=True)

  def __init__(self, name, age, gender, movie=[]):
    self.name = name
    self.age = age
    self.gender = gender
    self.movies = movie 

  def format(self):
    movies_data = [movie.title for movie in self.movies]
    return {
      'id': self.id,
      'name': self.name,
      'age': self.age,
      'gender': self.gender,
      'movies': movies_data}

  def insert(self):
    db.session.add(self)
    db.session.commit()
  
  def update(self):
    db.session.commit()

  def delete(self):
    # myparent.children.remove(somechild)
    db.session.delete(self)
    db.session.commit()

'''
Movie
Entity with title and release year
'''
class Movie(db.Model):  
  __tablename__ = 'Movie'

  id = Column(Integer, primary_key=True)
  title = Column(String, nullable=False)
  release_year = Column(DateTime, nullable=False)

  def __init__(self, title, release_year, actors=[]):
    self.title = title
    self.release_year = release_year
    self.actors = actors

  def format(self):
    actors_data = [actor.name for actor in self.actors]
    return {
      'id': self.id,
      'title': self.title,
      'release_year': self.release_year,
      'actors': actors_data}

  def insert(self):
    db.session.add(self)
    db.session.commit()
  
  def update(self):
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()
