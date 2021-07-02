from app import db
from app.models.card import Card
from app.models.board import Board
from flask import request, Blueprint, jsonify

cards_bp = Blueprint("cards", __name__, url_prefix="/boards")

def is_message_valid(message):
    return len(message) <= 40 and len(message) > 5

def build_card_response(card):
    return jsonify({"card": card.to_dict()})

def build_response(message):
    return jsonify({"details": message})

def invalid_message_len_response():
    return build_response("Length of the message schould be in [6,40] range")

def get_board(board_id):
    board = Board.query.get(board_id)
    if not board:
        return None, f"Board with id {board_id} not found"
    return board, None

def get_card(board_id, card_id):
    board, error = get_board(board_id)
    if error:
        return None, error
    card = Card.query.filter_by(board_id = board.board_id,  card_id=card_id).first()
    if not card:
        return None, f"Card with id {card_id} not found"
    return card, None

@cards_bp.route("<board_id>/cards/", methods = ["POST"], strict_slashes=False)
def add_card(board_id):
    """Adds a card to a board"""
    board, error = get_board(board_id)
    if error:
        return build_response(error)
    request_body = request.get_json() 
    # message = request_body["message"]
    message = request_body.message
    if not is_message_valid(message):
        return invalid_message_len_response()
    card = Card(message = message, board_id=board_id)
    db.session.add(card)
    db.session.commit()
    return build_card_response(card)

@cards_bp.route("<board_id>/cards/<card_id>", methods=["DELETE"], strict_slashes=False)
def delete_card(board_id, card_id):
    """Deletes a card with specified card id from a board with a specified board id"""
    card, error = get_card(board_id, card_id)
    if error:
        return build_response(error)
    card_message = card.message
    db.session.delete(card)
    db.session.commit()
    return build_response(f"Card with id {card_id} and message '{card_message}' was successfully deleted")

@cards_bp.route("<board_id>/cards/<card_id>/like", methods=["PATCH"], strict_slashes=False) 
def like_card(board_id, card_id):
    """Upvotes a card"""
    card, error = get_card(board_id, card_id)
    if error:
        return build_response(error)
    card.likes_count += 1
    db.session.commit()
    return build_card_response(card)

@cards_bp.route("<board_id>/cards/<card_id>/edit", methods=["PATCH"], strict_slashes=False) 
def edit_card(board_id, card_id):
    """Updates message of a single card"""
    card, error = get_card(board_id, card_id)
    if error:
        return build_response(error)
    request_body = request.get_json()
    message = request_body["message"]
    if not is_message_valid(message):
        return invalid_message_len_response()
    card.message = message
    db.session.commit()
    return build_card_response(card)
