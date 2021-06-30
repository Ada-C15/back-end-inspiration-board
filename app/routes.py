from flask import Blueprint, request, jsonify, make_response
from app import db
from app.models.card import Card
from app.models.board import Board

cards_bp = Blueprint("cards", __name__, url_prefix="/boards/<board_id>/cards")
boards_bp = Blueprint("boards", __name__, url_prefix="/boards")

@boards_bp.route("", methods=["GET"], strict_slashes=False)
def get_boards(): 
    boards = Board.query.all()
    boards_list = []
    for board in boards_list:
        boards_list.append({board.board_to_json_format})
    return jsonify(boards_list)

@boards_bp.route("", methods=["POST"], strict_slashes=False)
def add_board():
    board_post_request = request.get_json()
    new_board = Board(title=board_post_request["title"],
                    owner=board_post_request["owner"])
    db.session.add(new_board)
    db.session.commit()
    return jsonify({"board": new_board.board_to_json_format()}), 201


# @boards_bp.route("<board_id>/cards", methods=["GET"], strict_slashes=False)
# def get_cards():
#     pass

# @cards_bp.route("<board_id>/cards", methods=["POST"], strict_slashes=False)
# def add_cards():
#     pass

# The example implementation defines these endpoints.
# @boards_bp.route
# GET /boards
# POST /boards
# GET /boards/<board_id>/cards
# POST /boards/<board_id>/cards

# @cards_bp.route
# DELETE /cards/<card_id>
# PUT /cards/<card_id>/like