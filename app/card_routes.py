from flask import Blueprint, request, jsonify, make_response
from app import db

from app.models.card import Card
from app.models.board import Board


# cards_bp = Blueprint("card", __name__, url_prefix="/boards/<board_id>") ->?

cards_bp = Blueprint("cards", __name__, url_prefix="/boards")

# DELETE /cards/<card_id>
@cards_bp.route("/cards/<card_id>", methods=["GET"], strict_slashes=False)
def delete_card(board_id, card_id):
    # validate firsttt
    card_to_delete = Card.query.get(card_id)
    db.session.delete(card_to_delete)
    db.session.commit()
    # how to do the get or 404?
    return "deleted!", 200

# tried to add board and remove /cards/ as it's referenced @ board routes but I'm not sure about this endpoint
# PUT /cards/<card_id>/like
@cards_bp.route("/cards/<card_id>/like", methods=["GET"], strict_slashes=False)
def increase_likes(card_id): # board_id, card_id?
    # validate!!
    liked_card = Card.query.get(card_id)

    liked_card.likes_count  = liked_card.likes_count + 1
    # liked_card.likes_count +=1 !!!!?!?!?
    db.session.commit()
    return "successssss", 200


