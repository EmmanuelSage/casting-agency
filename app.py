import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, Movie, Actor

def create_app(test_config=None):
  # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    print('DDDDDDDDDDD',os.environ['ENV'])
    # setup cross origin
    CORS(app)

    # Setup home route
    @app.route('/')
    def welcome():
        return 'Welcome to casting agency'

    @app.route('/movies')
    def get_movies():
        movies = Movie.query.all()

        return jsonify({
            'success': True,
            'movies': [movie.format() for movie in movies],
        }), 200



    return app

APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)