from flask_script import Manager
from sqlalchemy import Column, String, Integer
from flask_migrate import Migrate, MigrateCommand
from datetime import datetime

from app import create_app
from models import db, Movie, Actor

app = create_app()

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

@manager.command
def seed():
    pass

if __name__ == '__main__':
    manager.run()
