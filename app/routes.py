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

# PRIORITY FOR TODAY
# GET / boards / <board_id> / cards 
# @board_bp.route("/<board_id>/cards", methods=["GET"])
# def get_cards_for_board(board_id):
#     board = Board.query.get(board_id)

#     if board is None:
#         return ("Board does not exist (1)", 404)

#     cards = Card.query.filter_by(board=board_id)
#     card_list = []
#     for card in cards:
#         card_list.append(card.board_json())

#     return make_response({
#         "id": board.board_id,
#         "title": board.title,
#         "cards": card_list
#     }, 200)


# POST / boards / <board_id> / cards - (FULLY FUNCTIONING, DON'T TOUCH THIS! LOVE YOU, BUT DON'T TRUST YOU!)
@board_bp.route("/<board_id>/cards", methods=["POST"])
def create_cards_for_board(board_id):
    request_body = request.get_json()

    if "message" not in request_body:
        return make_response({"details": "Invalid data"}, 400)

    new_card = Card(message=request_body["message"], board_id=board_id)

    db.session.add(new_card)
    db.session.commit()

    return make_response(new_card.card_json())

# NOT PRIORITY, BUT NICE TO HAVE TODAY
# DELETE / cards / <card_id> 
#@card_bp.route("/<card_id>", methods=["DELETE"])
#def delete_card(card_id):

# NOT PRIORITY, BUT NICE TO HAVE TODAY
# # PUT / cards / <board_id> / like
# @card_bp.route("cards/<board_id>/like", methods=["PUT"])
# def like_card(board_id):