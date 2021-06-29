from flask import Blueprint, request, jsonify, make_response
from app import db
from app.models.card import Card
from app.models.board import Board
# from datetime import datetime
# import requests
# import os

# example_bp = Blueprint('example_bp', __name__)

cards_bp = Blueprint("cards", __name__, url_prefix="/cards")
boards_bp = Blueprint("boards", __name__, url_prefix="/boards")