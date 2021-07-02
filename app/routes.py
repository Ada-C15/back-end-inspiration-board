from flask import Blueprint, request, jsonify, make_response
from app.models.board import Board
from app.models.card import Card
from app import db
# import requests
import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import random

boards_bp = Blueprint("boards", __name__, url_prefix="/boards")
cards_bp = Blueprint("cards", __name__, url_prefix="/cards")


#=====================================================#
#                   BOARD ROUTES                      #
#=====================================================#

@boards_bp.route("", methods=["GET"], strict_slashes=False)
def list_all_boards():
    boards = Board.query.all()
    boards_response = [board.to_json() for board in boards]
    return jsonify(boards_response), 200

@boards_bp.route("", methods=["POST"])
def add_new_board(): 
    request_body = request.get_json()
    try:
        request_body["title"]
        request_body["owner"]
    except:
        return jsonify({
            "details": "Invalid data"
        }), 400
    new_board = Board(
            title=request_body["title"],
            owner=request_body["owner"]
            )
    db.session.add(new_board)
    db.session.commit()
    return make_response(new_board.to_json(), 201)

def call_slack_api(new_card):
    client = WebClient(token=os.environ.get("SLACK_BOT_TOKEN"))
    channel_id = "buggy-puggy"
    # try:
    AFFIRMATIONS = [
        f"So Fetch! New card #{new_card.card_id} posted: '{new_card.message}'", 
        f"So Grool! New card #{new_card.card_id} posted: '{new_card.message}'", 
        f"You go Glenn Coco! New card #{new_card.card_id} posted: '{new_card.message}'", 
        f"The limit does not exist, but on here it is 40 characters (HERE)! New card #{new_card.card_id} posted!", 
        f"Your face smells like peppermint (and other compliments) (HERE)! New card #{new_card.card_id} posted!", 
        f"Get in loser. We're going compliment shopping (HERE)! New card #{new_card.card_id} posted!", 
    ]
    affirmation_quote = AFFIRMATIONS[random.randint(0,len(AFFIRMATIONS)-1)]
    result = client.chat_postMessage(
        channel=channel_id,
        text=f"{affirmation_quote}")
        # text=f"New card #{new_card.card_id} posted! Check if someone talked smack about you! 💀 XOXO💋")
    return result


@boards_bp.route("/<int:board_id>/cards", methods=["POST"])
def add_new_card_to_board(board_id): 
    request_body = request.get_json()
    try:
        request_body["message"]
    except:
        return jsonify({
            "details": "Invalid data" 
        }), 400
    if len(request_body["message"]) > 40 or request_body["message"] == "": 
        return jsonify({
            "details": "Message must be between 1 to 40 characters long"
        }), 400
    new_card = Card(
            message=request_body["message"],
            board_id=board_id
            )
    db.session.add(new_card)
    db.session.commit()

    return make_response(new_card.to_json(), 201)

@boards_bp.route("/<int:board_id>/cards", methods=["GET"], strict_slashes=False)
def get_cards_of_one_board(board_id):
    board = Board.query.get_or_404(board_id)
    board_response = board.to_json()
    board_response["cards"] = [card.to_json() for card in board.cards]
    return jsonify(board_response), 200


#=====================================================#
#                    CARD ROUTES                      #
#=====================================================#

@cards_bp.route("/<int:card_id>", methods=["DELETE"], strict_slashes=False)
def delete_card(card_id):
    card = Card.query.get_or_404(card_id)
    db.session.delete(card)
    db.session.commit()
    card_response = {
        "details": f'Card {card.card_id} successfully deleted'
        }
    return make_response(card_response), 200 
    

@cards_bp.route("/<int:card_id>/like", methods=["PUT"], strict_slashes=False)
def updating_card_likes_count(card_id):
    card = Card.query.get_or_404(card_id)
    # request_body = request.get_json()
    card.likes_count+=1
    # card.likes_count=request_body["likes_count"]
    db.session.commit()
    likes_response = {
        "details": f"Updated {card.card_id}'s likes count to {card.likes_count}"
        }
    return make_response(likes_response), 200

