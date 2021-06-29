from flask import Blueprint, request, jsonify, make_response
# from flask.signals import request_finished
from app import db
from app.models.board import Board
from app.models.card import Card
import os
import requests


# example_bp = Blueprint('example_bp', __name__)
board_bp = Blueprint("boards", __name__, url_prefix="/boards")
card_bp = Blueprint("cards", __name__, url_prefix="/cards")

# GET / boards - (FULLY FUNCTIONING, DON'T TOUCH THIS! LOVE YOU, BUT DON'T TRUST YOU!)
@board_bp.route("", methods=["GET"])
def get_boards():
    boards = Board.query.all()
    boards_response = []
    for board in boards:
        boards_response.append(board.board_json())

    return jsonify(boards_response)

# POST / boards - (FULLY FUNCTIONING, DON'T TOUCH THIS! LOVE YOU, BUT DON'T TRUST YOU!)
@board_bp.route("", methods=["POST"])
def create_board():
    request_body = request.get_json()

    board_properties = ["title", "owner"]
    for prop in board_properties:
        if prop not in request_body:
            return make_response({"details": "Invalid data"}, 400)

    new_board = Board(title=request_body["title"],
                    owner=request_body["owner"])

    db.session.add(new_board)
    db.session.commit()

    return make_response(new_board.board_json())

# (FULLY FUNCTIONING, DON'T TOUCH THIS! LOVE YOU, BUT DON'T TRUST YOU!)
# GET / boards / <board_id> / cards 
@board_bp.route("/<board_id>/cards", methods=["GET"])
def get_cards_for_board(board_id):
    board = Board.query.get(board_id)

    # if board is None:
    #     return ("Board does not exist", 404)

    if board is None:
        return make_response("Board does not exist", 404)

    return make_response(board.return_board_cards())

# POST / boards / <board_id> / cards 
# (FULLY FUNCTIONING, DON'T TOUCH THIS! LOVE YOU, BUT DON'T TRUST YOU!)
@board_bp.route("/<board_id>/cards", methods=["POST"])
def create_cards_for_board(board_id):
    request_body = request.get_json()

    if "message" not in request_body:
        return make_response({"details": "Invalid data"}, 400)

    new_card = Card(message=request_body["message"], board_id=board_id)

    db.session.add(new_card)
    db.session.commit()

    return make_response(new_card.card_json())


# DELETE / cards / <card_id> 
@card_bp.route("/<card_id>", methods=["DELETE"])
def delete_card(card_id):
    card = Card.query.get(card_id)

    db.session.delete(card)
    db.session.commit()

    return {
            "details":\
            (f"Card {card_id} successfully deleted")
            }


# PUT / cards / <card_id> / like
@card_bp.route("/<card_id>/like", methods=["PUT"])
def like_card(card_id):
    card = Card.query.get(card_id)
    request_body = request.get_json()

    card.likes_count = request_body["likes_count"]
    card.likes_count += 1
    db.session.commit()

    return make_response(card.card_json())

