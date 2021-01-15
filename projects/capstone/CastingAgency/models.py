from sqlalchemy import Column, String, create_engine
from flask_sqlalchemy import SQLAlchemy
import json
import os

database_path = os.environ['DATABASE_URL']

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


class Movie(db.Model):  
    __tablename__ = 'movie'

    id = Column(db.Integer, primary_key=True)
    title = Column(db.String, unique=True, nullable=False)
    release_date = Column(db.String)

    def format(self):
        return {
        'id': self.id,
        'title': self.title,
        'release_date': self.release_date}

class Actor(db.Model):
    __tablename__ = 'actor'

    id = Column(db.Integer, primary_key=True)
    name = Column(db.String, nullable=False)
    age = Column(db.Integer)
    gender = Column(db.String)

    def format(self):
        return {
        'id': self.id,
        'name': self.name,
        'age': self.age,
        'gender': self.gender}