from flask import Blueprint, request, jsonify, make_response, json
from flask.signals import request_finished
from app import db
from app.models.board import Board
from app.models.card import Card
import os
import re
import requests


# example_bp = Blueprint('example_bp', __name__)
board_bp = Blueprint("board", __name__, url_prefix="/boards")
card_bp = Blueprint("cards", __name__, url_prefix="/cards")

# GET / boards
@board_bp.route("", methods=["GET"])
def get_boards():
    boards = Board.query.all()
    boards_response = []
    for board in boards:
      boards_response.append(board.board_json())

    return jsonify(boards_response)

# POST / boards
@board_bp.route("", methods=["POST"])
def create_board():
    request_body = request.get_json()
    if "title" or "owner" not in request_body:
        return make_response({"details": "Invalid data"}, 400)

    new_board = Board(title=request_body["title"],
                      owner=request_body["owner"])

    db.session.add(new_board)
    db.session.commit()

    return make_response({"id": new_board.board_id}, 200)

# GET / boards / <board_id> / cards
@board_bp.route("<board_id>/cards", methods=["GET"])
def get_cards_for_board(board_id):
    board = Board.query.get(board_id)

    if board is None:
        return ("Board does not exist (1)", 404)

    cards = Card.query.filter_by(board=board_id)
    card_list = []
    for card in cards:
      card_list.append(card.board_json())

    return make_response({
      "id": board.board_id,
      "title": board.title,
      "owner": board.owner,
      "card": card_list
    }, 200)

# POST / boards / <board_id> / cards
@board_bp.route("<board_id>/cards", methods=["POST"])
def create_cards_for_board(board_id):
    board = Board.query.get(board_id)

    if board is None:
        return ("Board does not exist (2)", 404)
    
    request_body = request.get_json()
    for card_id in request_body["card_id"]:
      card = Card.query.get(card_id)
      card.board = board.board_id

    return make_response({
      "id": board.board_id,
      "card_id": request_body["card_id"]
      }, 200)

# DELETE / cards / <card_id> 
#@card_bp.route("/<card_id>", methods=["DELETE"])
#def delete_card(card_id):


# # PUT / cards / <board_id> / like
# @card_bp.route("cards/<board_id>/like", methods=["PUT"])