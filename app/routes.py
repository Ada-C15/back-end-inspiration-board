from flask import Blueprint, request, jsonify, make_response
from werkzeug.wrappers import response
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
cards_bp = Blueprint("cards", __name__, url_prefix="/cards")


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


@boards_bp.route("/<board_id>/cards", methods=["POST"], strict_slashes=False)
# Body should be a json like: { "card_ids": [1, 2]}
# Returns a json with board_id and all the cards linked to that board
def create_card_ids_to_board(board_id):
    request_body = request.get_json()
    board = Board.query.get_or_404(board_id)
    for search_card_id in request_body["card_ids"]:
        card = Card.query.get(search_card_id)
        card.board_id = board_id
    db.session.commit()
    response = {
        "board_id" : board_id,
        "card_ids": request_body["card_ids"]
    }
    return jsonify(response), 200


@boards_bp.route("/<board_id>/cards", methods=["GET"], strict_slashes=False)
def get_cards_for_one_board(board_id):
    board = Board.query.get_or_404(board_id, "Incorrect id")
    cards = board.cards
    cards_response = []
    for card in cards:
        cards_response.append(card.card_json())
    response = {
        "id": board.board_id,
        "title": board.title,
        "cards": cards_response
    }
    return jsonify(response), 200




# ***************************** CARD ROUTES ***********************

@cards_bp.route("", methods=["POST"], strict_slashes=False)
def post_card():
    request_body = request.get_json()
    new_card = Card(message= request_body["message"])
    
    if new_card.message == "" \
        or type(new_card.message) is not str:
        return 404
    else:
        db.session.add(new_card)
        db.session.commit()
        response = {
            "id" : new_card.card_id
        }
        return make_response(response, 201)


@cards_bp.route("/<card_id>", methods= ["DELETE"], strict_slashes=False)
def delete_card(card_id):
    card = Card.query.get_or_404(card_id)
    db.session.delete(card)
    db.session.commit()

    return make_response(f"Card with ID: {card.card_id} deleted", 200)


@cards_bp.route("/<card_id>/likes", methods= ["PUT"], strict_slashes=False)
def add_likes(card_id):
    card = Card.query.get_or_404(card_id)
    form_data = request.get_json()
    likes_count = form_data["likes_count"]
    
    db.session.commit()

    return make_response(f"Likes count has been updated to: {likes_count}", 200)


