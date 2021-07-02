from flask import Blueprint, request, jsonify, make_response
from app import db

from app.models.card import Card
from app.models.board import Board


cards_bp = Blueprint("cards", __name__, url_prefix="/boards")

# @cards_bp.route("<board_id>/cards/<card_id>", methods=["DELETE"], strict_slashes=False)
# def delete_card(board_id, card_id):
#     card_to_delete = Card.query.get(card_id)
#     db.session.delete(card_to_delete)
#     db.session.commit()
#     return "deleted!", 200

# @cards_bp.route("<board_id>/cards/<card_id>/likes", methods=["PUT"], strict_slashes=False)
# def increase_likes(card_id): # board_id, card_id?
#     liked_card = Card.query.get(card_id)

#     liked_card.likes_count  = liked_card.likes_count + 1
#     # liked_card.likes_count +=1 ?
#     db.session.commit()
#     return "successssss", 200

# GET /boards/<board_id>/cards
@cards_bp.route("/<board_id>/cards", methods=["GET"], strict_slashes=False)
def get_cards(board_id):
    current_board = Board.query.get(board_id) #!!???
    # needs validachon
    #so close we got this I'm sorry i just noticed this, I will come back to it later if I have time or if you want me to -laurel 
    return jsonify(current_board.cards_list_to_json()), 200


# POST /boards/<board_id>/cards
@cards_bp.route("<board_id>/cards", methods=["POST"], strict_slashes=False)
def add_card(board_id):

    current_board = Board.query.get(board_id)
    response = request.get_json() 

    new_card = Card(
                message=response["message"],

                # should the likes_count have a default value of 0?
                # I added a default value of 0 to the card model on line 11
                # I commented out line 64 and the post request works with just the "message" in the post request 
                # likes_count=likes_count,
                board_id=board_id)
    
    db.session.add(new_card)

    current_board.cards.append(new_card)
    db.session.add(current_board)
    db.session.commit()

    # not sure if this is a preference, but line 74 returns a list 
    # should we return just the 1 card each post request? 
    # return jsonify(current_board.cards_list_to_json()), 201

    return jsonify(new_card.card_to_json()), 201


# Delete a single card
@cards_bp.route("<board_id>/cards/<card_id>", methods=["DELETE"], strict_slashes=False)
def delete_card(board_id, card_id):
    card_to_delete = Card.query.get(card_id)
    db.session.delete(card_to_delete)
    db.session.commit()
    return "deleted!", 200

# increase likes of a card 
@cards_bp.route("<board_id>/cards/<card_id>/likes", methods=["POST"], strict_slashes=False)
def increase_likes(board_id, card_id): 
    current_board = Board.query.get(board_id)
    current_card = Card.query.get(card_id)
    if current_board.board_id == current_card.board_id:
        current_card.likes_count += 1
    db.session.add(current_card)
    db.session.commit()
    return jsonify(current_card.card_to_json()), 200


