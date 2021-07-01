from flask import Blueprint, request, jsonify, make_response
# from flask.signals import request_finished
from app import db
from app.models.board import Board
from app.models.card import Card
from app import slack_key
import os
import requests
from flask_cors import CORS, cross_origin


# example_bp = Blueprint('example_bp', __name__)
board_bp = Blueprint("boards", __name__, url_prefix="/boards")
card_bp = Blueprint("cards", __name__, url_prefix="/cards")

# GET / boards - (FULLY FUNCTIONING, DON'T TOUCH THIS! LOVE YOU, BUT DON'T TRUST YOU!)
@board_bp.route("", methods=["GET"])
@cross_origin()
def get_boards():
    boards = Board.query.all()
    boards_response = []
    for board in boards:
        boards_response.append(board.board_json())

    return make_response(boards_response)

# POST / boards - (FULLY FUNCTIONING, DON'T TOUCH THIS! LOVE YOU, BUT DON'T TRUST YOU!)
@board_bp.route("", methods=["POST"])
@cross_origin()
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
@cross_origin()
def get_cards_for_board(board_id):
    board = Board.query.get(board_id)

    if board is None:
        return make_response("Board does not exist", 404)

    return make_response(board.return_board_cards())

# POST / boards / <board_id> / cards 
# (FULLY FUNCTIONING, DON'T TOUCH THIS! LOVE YOU, BUT DON'T TRUST YOU!)
@board_bp.route("/<board_id>/cards", methods=["POST"])
@cross_origin()
def create_cards_for_board(board_id):
    request_body = request.get_json()

    if "message" not in request_body:
        return make_response({"details": "Invalid data"}, 400)

    new_card = Card(message=request_body["message"], board_id=board_id)

    db.session.add(new_card)
    db.session.commit()
    created_card_id = new_card.card_id
    slack_notification(created_card_id)

    return make_response(new_card.card_json())

# PATCH / boards / <board_id> / cards
# Every time a new card is made, it sends a message to the team's public Slack channel
@board_bp.route("/<board_id>/cards", methods=["PATCH"])
@cross_origin()
def slack_notification(created_card_id):
    card = Card.query.get(created_card_id)
    board = Board.query.get(card.board_id)

    url = "https://slack.com/api/chat.postMessage"
    data = {
        "channel": "team-6-inspo",
        "text": (f"🥳✨ Someone just created a new card with message '{card.message}' on board '{board.title}' ✨ 🙌") 
    }
    headers = {
        "Authorization": f"Bearer {slack_key}"
    }

    requests.post(url, data=data, headers=headers)

    return make_response("Card created", 201)


    # return make_response({"card": card.card_json()})

# DELETE / cards / <card_id> 
@card_bp.route("/<card_id>", methods=["DELETE"])
@cross_origin()
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
@cross_origin()
def like_card(card_id):
    
    card = Card.query.get(card_id)
    card.likes_count += 1
    db.session.commit()

    return make_response(card.card_json())


