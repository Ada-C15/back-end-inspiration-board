from flask import Blueprint, request, jsonify, make_response
from app.models.card import Card
from app.models.board import Board
from app import db

boards_bp = Blueprint("boards", __name__, url_prefix="/boards")
cards_bp = Blueprint("cards", __name__, url_prefix="/cards")

# Get all boards
@boards_bp.route("", methods=["GET"])
def get_all_boards():
    query = Board.query.order_by(Board.board_id.asc())

    boards_list = []
    for board in query:
        boards_list.append(board.get_resp())

    return jsonify(boards_list), 200 

# Create a board
@boards_bp.route("", methods=["POST"])
def create_board():
    request_body = request.get_json()
    new_board = Board(
        title=request_body["title"],
        owner=request_body["owner"]
    )
    db.session.add(new_board)
    db.session.commit()
    return (jsonify(f"Posted new board {new_board.title}!"),201)



'''
Next: Create, Read, and Delete Cards
'''
# Gets all cards
@cards_bp.route("", methods=["GET"])
def get_all_card():
    query = Card.query.order_by(Card.card_id.asc())
    cards_list = []
    for card in query:
        cards_list.append(card.get_resp())
    return jsonify(cards_list), 200 

# Get all cards associated with board
@cards_bp.route("/<board_id>", methods=["GET"])
def get_card(board_id):
    board = Board.query.get(board_id)
    cards_list = []
    for card in board.cards:
        board_card = Card.query.get(card.card_id)

        cards_list.append(board_card.get_resp())
    return (jsonify(cards_list),201)

# Create a card for a board
@cards_bp.route("/<board_id>", methods=["POST"])
def create_card(board_id):
    request_body = request.get_json()
    new_card = Card(
        message=request_body["message"],
        board_id=board_id
    )
    db.session.add(new_card)
    db.session.commit()
    return (jsonify(f"Posted new card on board {new_card.board_id}!"),201)

# # Delete a card 
# @cards_bp.route("/<board_id>", methods=["DELETE"])
# def delete_card(board_id):
#     pass