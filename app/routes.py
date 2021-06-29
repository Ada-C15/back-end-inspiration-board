from flask import Blueprint, request, jsonify, make_response
from app import db
from .models.board import Board
from .models.card import Card


board_bp = Blueprint("boards", __name__, url_prefix="/boards")
card_bp = Blueprint("cards", __name__, url_prefix="/cards")

@board_bp.route("", methods=["POST"], strict_slashes=False)
def create_board():
    request_body=request.get_json()
    if "title" in request_body and "owner" in request_body:
        new_board = Board(title= request_body["title"],
                            owner= request_body["owner"])
        db.session.add(new_board)
        db.session.commit()

        return make_response({"board": new_board.to_dict()}, 201)
    
    elif "title" not in request_body:
        return make_response({"details": "Title data invalid"}, 400)
    
    elif "owner" not in request_body:
        return make_response({"details": "Owner data invalid"}, 400)

@board_bp.route("", methods=["GET"], strict_slashes=False)
def get_boards():
    boards = Board.query.all()
    boards_response = [board.to_dict() for board in boards]
    return make_response(jsonify(boards_response), 200)


@board_bp.route("/<board_id>/cards", methods=["POST"], strict_slashes=False)
def add_card_to_board(board_id):
    request_body=request.get_json()
    
    if "message" in request_body and "likes_count" in request_body:
        new_card = Card(message= request_body["message"],
                            likes_count= request_body["likes_count"],
                            board_id= int(board_id))
        db.session.add(new_card)
        db.session.commit()    

        return make_response({"card": new_card.to_dict()},201)   

    elif "message" not in request_body:
        return make_response({"details": "Message data invalid"}, 400)
    
    elif "likes_count" not in request_body:
        return make_response({"details": "Likes_count data invalid"}, 400)
    # likes_count might need to be refactors to default to zero when new card is created!!

@board_bp.route("/<board_id>/cards", methods=["GET"], strict_slashes=False)
def get_cards_from_board(board_id):
    cards = Card.query.filter_by(board_id=board_id)
    if cards:
        cards_response = [card.to_dict() for card in cards]
        return make_response({"cards": cards_response}, 200)
    return make_response("", 200)

@card_bp.route("/<card_id>", methods=["DELETE"], strict_slashes=False)
def remove_card(card_id):
    card = Card.query.get(card_id)
    if card:
        db.session.delete(card)
        db.session.commit()
        return jsonify({
            "details": (f'Card {card.card_id} successfully deleted from Board {card.board_id}')
        }), 200
    return "", 404