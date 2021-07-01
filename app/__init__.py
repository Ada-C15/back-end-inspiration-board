from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import os
from flask_cors import CORS, cross_origin

db = SQLAlchemy()
migrate = Migrate()
load_dotenv()
slack_key = os.environ.get("SLACK_API_KEY")


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
        "SQLALCHEMY_DATABASE_URI")

    # Import models here for Alembic setup
    # from app.models.ExampleModel import ExampleModel
    from app.models.board import Board
    from app.models.card import Card

    db.init_app(app)
    migrate.init_app(app, db)

    # Register Blueprints here
    # from .routes import example_bp
    # app.register_blueprint(example_bp)
    from .routes import board_bp
    app.register_blueprint(board_bp)

    from .routes import card_bp
    app.register_blueprint(card_bp)


    CORS(app, resources={r"/api/*":{"origins":"*"}})
    app.config['CORS_HEADERS'] = 'Content-Type'
    return app
