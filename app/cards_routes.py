from app import db
from app.models.card import Card
from app.models.board import Board
from flask import request, Blueprint, jsonify

# Q: do we need the codes?
# Q: jsonify and make_response
# get_or_404
# strict 

cards_bp = Blueprint("cards", __name__, url_prefix="/boards/<board_id>/cards")

def get_card_response(card):
    """Returns card's data"""
    return jsonify({"card": card.to_dict()})

def get_error_response(card_id):
    """Returns error message"""
    return jsonify({"details": f"Card with id {card_id} is not found"})

@cards_bp.route("", methods = ["POST"])
def add_card():
    """Adds a card to a board"""
    request_body = request.get_json() 
    if len(request_body["message"]) > 40:
        return jsonify({"details": f"Your message is too long"})
    if len(request_body["message"]) == 0:
        return jsonify({"details": f"You can't submit an empty card"})
    card = Card(message = request_body["message"])
    db.session.add(card)
    db.session.commit()
    return get_card_response(card)

@cards_bp.route("/<card_id>", methods=["DELETE"])
def delete_card(card_id):
    """Deletes a card"""
    card = Card.query.get(card_id)
    if not card:
        return get_error_response(card_id)
    db.session.delete(card)
    db.session.commit()
    return ({"details": f"Card {card_id} \"{card.message}\" successfully deleted"})

@cards_bp.route("/<card_id>", methods=["PATCH"]) # used patch instead of put
def update_card(card_id):
    """Updates a portion of a single card"""
    card = Card.query.get(card_id)
    if not card:
        return get_error_response(card_id)
    request_body = request.get_json()
    # Updates message
    if request_body["message"]: #update
        card.message = request_body["message"]
    # Updates likes count
    else:
        card.likes_count += 1
    db.session.commit()
    return get_card_response(card)






board = Board.query.get_or_404(board_id)
cards = Card.query.filter_by(board_id=board.board_id)
card = cards.query.get_or_404(card_id)




