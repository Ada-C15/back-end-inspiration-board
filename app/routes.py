from flask import Blueprint, request, jsonify, make_response
from app import db
import requests
from flask import jsonify
from .models.board import Board
from app.models.card import Card
from dotenv import load_dotenv
from sqlalchemy import exc

load_dotenv()

# example_bp = Blueprint('example_bp', __name__)
boards_bp = Blueprint("board", __name__, url_prefix="/boards")
cards_bp = Blueprint("cards", __name__, url_prefix="cards")


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


@boards_bp.route("", methods=["GET"], strict_slashes=False)
def get_boards():
    boards_response = []
    boards = Board.query.all()
    for board in boards:
        boards_response.append(board.to_json())
    return jsonify(boards_response), 200


@boards_bp.route("/<board_id>", methods=["GET"], strict_slashes=False)
def get_one_board(board_id):
    board = Board.query.get_or_404(board_id, "Incorrect id")
    return make_response(board.to_json(), 200)


# ***************************** CARD ROUTES ***********************

@cards_bp.route("/<board_id>", methods=["POST"], strict_slashes=False)
def post_card():
    request_body = request.get_json()
    new_card = Card(message= request_body["message"])
    
    if new_card["message"] == "" \
        or type(new_card["message"]) is not str:
        return 404
    else:
        db.session.add(new_card)
        db.session.commit()
        return make_response

