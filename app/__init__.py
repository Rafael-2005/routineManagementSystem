from flask import Flask
from flask_migrate import Migrate
from .database import db
from .routes import main

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    Migrate(app, db)

    app.register_blueprint(main)

    return app