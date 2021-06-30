from app import db
from app.models.card import Card
from app.models.board import Board
from flask import request, Blueprint, jsonify

# Q: do we need the codes?
# Q: jsonify and make_response
# get_or_404

cards_bp = Blueprint("cards", __name__, url_prefix="/boards/board_id/cards")

def cards_data(card):
    return jsonify({"card": card.to_dict()})

def card_not_found(card_id):
    return jsonify({"details": f"Card with id {card_id} is not found"})

def message_valid(length):
    if length > 40 or length <= 5:
        return False
    return True

def not_valid_message():
    return jsonify({"details": "Just try to refrase :)"})

@cards_bp.route("", methods = ["POST"], strict_slashes=False)
def add_card():
    """Adds a card to a board"""
    request_body = request.get_json() 
    length = len(request_body["message"])
    if not message_valid(length):
        return not_valid_message()
    card = Card(message = request_body["message"])
    db.session.add(card)
    db.session.commit()
    return cards_data(card)

@cards_bp.route("/<card_id>", methods=["DELETE"], strict_slashes=False)
def delete_card(card_id):
    """Deletes a card"""
    card = Card.query.get(card_id)
    if not card:
        return card_not_found(card_id)
    db.session.delete(card)
    db.session.commit()
    return ({"details": f"Card {card_id} \"{card.message}\" successfully deleted"})

@cards_bp.route("/<card_id>/like", methods=["PATCH"], strict_slashes=False) 
def like_card(card_id):
    """Upvotes a card"""
    card = Card.query.get(card_id)
    if not card:
        return card_not_found(card_id)
    card.likes_count += 1
    db.session.commit()
    return cards_data(card)

@cards_bp.route("/<card_id>/edit", methods=["PATCH"], strict_slashes=False) 
def edit_card(card_id):
    """Updates message of a single card"""
    card = Card.query.get(card_id)
    if not card:
        return card_not_found(card_id)
    request_body = request.get_json()
    length = len(request_body["message"])
    if not message_valid(length):
        return not_valid_message()
    card.message = request_body["message"]
    db.session.commit()
    return cards_data(card)



"""
board = Board.query.get_or_404(board_id)
cards = Card.query.filter_by(board_id=board.board_id)
card = cards.query.get_or_404(card_id)
"""



