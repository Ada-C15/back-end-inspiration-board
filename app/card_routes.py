from flask import Blueprint, request, jsonify, make_response
from app import db

from app.models.card import Card
from app.models.board import Board


cards_bp = Blueprint("cards", __name__, url_prefix="/boards")

@cards_bp.route("<board_id>/cards/<card_id>", methods=["DELETE"], strict_slashes=False)
def delete_card(board_id, card_id):
    card_to_delete = Card.query.get(card_id)
    db.session.delete(card_to_delete)
    db.session.commit()
    return "deleted!", 200

@cards_bp.route("<board_id>/cards/<card_id>/likes", methods=["PUT"], strict_slashes=False)
def increase_likes(card_id): # board_id, card_id?
    liked_card = Card.query.get(card_id)

    liked_card.likes_count  = liked_card.likes_count + 1
    # liked_card.likes_count +=1 ?
    db.session.commit()
    return "successssss", 200


