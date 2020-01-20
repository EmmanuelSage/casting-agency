import os
from sqlalchemy import Column, String, Integer, DateTime
from flask_sqlalchemy import SQLAlchemy

# get database url from environment
db_url = os.environ['DATABASE_URL']
test_url = os.environ['TEST_DATABASE_URL']
env = os.environ['ENV']


# Use test database if environment is set to test
database_url = test_url if env == 'test' else db_url

# instanciate SQLALchemy as db
db = SQLAlchemy()


# Setup database config
def setup_db(app, database_url=database_url):
    """setup database configuration for flask application"""
    app.config["SQLALCHEMY_DATABASE_URI"] = database_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)


# Setup Movie model inherits from db.model;
class Movie(db.Model):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True)
    title = Column(String(120), unique=True, nullable=False)
    release_date = Column(DateTime(), nullable=False)

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date,
            }


# Setup Actor model inherits from db.model;
class Actor(db.Model):
    __tablename__ = 'actors'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String, nullable=False)

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender
            }
