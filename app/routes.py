from flask import Blueprint, request, jsonify, make_response
from app import db
import requests
from flask import jsonify
from .models.board import Board
from dotenv import load_dotenv
from sqlalchemy import exc


# example_bp = Blueprint('example_bp', __name__)
boards_bp = Blueprint("board", __name__, url_prefix="/boards")


"""
CRUD FOR BOARD
"""

@boards_bp.route("", methods=["POST"], strict_slashes=False)
def create_board():
    #Reads the HTTP request boby with:
    request_body = request.get_json()

    if len(request_body) == 2:
        new_board = Board(title = request_body["title"], owner = request_body["owner"])
        db.session.add(new_board)
        db.session.commit()
        response = {
            "id" : new_board.board_id
        }
        return make_response(jsonify(response),201)
    
    elif ("title" not in request_body) or ("owner" not in request_body):
        response = {
            "error": "Invalid data"
        }
        return make_response(response,400)