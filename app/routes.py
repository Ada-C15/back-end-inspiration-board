from flask import Blueprint, request, jsonify, make_response
from app import db
from .models.board import Board
from .models.card import Card
from flask import request, Blueprint, make_response, jsonify



boards_bp = Blueprint("board", __name__, url_prefix="/boards")

@boards_bp.route("", methods=["GET"], strict_slashes=False)
def boards():
    if request.method == "GET":
        board_list = []

        for board in board_list: 
            board_list.append({
                "id": board.board_id,
                "title": board.title,
                "owner": board.owner,
                
            })
            
        return jsonify(board_list)

@boards_bp.route("<board_id>/cards", methods=["POST", "GET"], strict_slashes=False) # get all cards for specific board
def handle_board_cards(board_id):

    board = Board.query.get(board_id) # get correct board using id passed into endpoint

    if board is None: # if board doesn't exist, return error
        return "", 404

    if request.method == "POST": # post card to one board

        request_body = request.get_json() # deviated from Task List API logic here
        
        new_card = Card(message=request_body["message"],
                        likes_count=request_body["likes_count"]) # this is going to have to become logic

        new_card.board_id = board_id # assign board id to new instance of/row in Card

        db.session.commit()

        return {
            "board_id": board.board_id,
            "card_id": new_card.card_id # we might be returning something else here
        }

    if request.method == "GET": # get cards of one board

        associated_cards = Card.query.filter_by(board_id=board_id)

        list_of_cards = []

        for card in associated_cards:
            list_of_cards.append({
                "card_id": card.card_id,
                "board_id": card.board_id,
                "message": card.message,
                "likes_count": card.likes_count,
        })

        return {
            "board_id": board.board_id, # board data was obtained on line 29
            "board_title": board.title,
            "cards": list_of_cards
            }


cards_bp = Blueprint("cards", __name__, url_prefix="/cards")

@boards_bp.route("/<card_id>", methods=["DELETE"], strict_slashes=False)
def cards(card_id):

    card = Card.query.get(card_id)

    if card is None:
        return "", 404

    db.session.delete(card)
    db.session.commit()

    return jsonify({
        "details": f'Card {card.card_id} "{card.title}" successfully deleted.'
    }) 
