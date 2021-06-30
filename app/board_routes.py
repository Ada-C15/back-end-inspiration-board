
from flask import Blueprint, request, jsonify
from app import db
from app.models.card import Card
from app.models.board import Board



boards_bp = Blueprint("boards", __name__, url_prefix="/boards")

# GET /boards
@boards_bp.route("", methods=["GET"], strict_slashes=False)
def get_boards():
    all_boards = Board.query.all()
    boards_list = []
    for board in all_boards:
        boards_list.append(board.board_to_json())
    return jsonify({"boards_list": boards_list}), 200


# POST /boards
@boards_bp.route("", methods=["POST"], strict_slashes=False)
def add_board():
    response = request.get_json()
    # validate!

    new_board = Board(title=response["title"],
                    owner=response["owner"])

    db.session.add(new_board)
    db.session.commit()

    return jsonify(new_board.board_to_json()), 201


# GET /boards/<board_id>/cards
@boards_bp.route("/<board_id>/cards", methods=["GET"], strict_slashes=False)
def get_cards(board_id):
    current_board = Board.query.get(board_id) #!!???
    # needs validachon
    return jsonify(current_board.cards_list_to_json()), 200


# POST /boards/<board_id>/cards
@boards_bp.route("<board_id>/cards", methods=["POST"], strict_slashes=False)
def add_card(board_id):
    current_board = Board.query.get(board_id)
    response = request.get_json() # board_request!!!
    # check if board exists by referencing board by ID
    # if not SOMEHTING in cards_to_add:
    #     return 404
    # not valid yet!

    new_card = Card(message=response["message"],
                likes_count=response["likes_count"],
                board=board_id)
    db.session.add(new_card)

    current_board.cards.append(new_card)
    db.session.add(current_board)
    db.session.commit()

    # return jsonify(available_board.cards_list()), 201
    return "SUCCESSS", 201



