from flask import Blueprint, request, jsonify, make_response
from app import db
from app.models.card import Card
from app.models.board import Board

cards_bp = Blueprint("cards", __name__, url_prefix="/cards")
boards_bp = Blueprint("boards", __name__, url_prefix="/boards")

# not tested
@boards_bp.route("", methods=["GET"], strict_slashes=False)
def get_boards(): # gets all boards?
    boards = Board.query.all()
    boards_list = []
    for board in boards_list:
        boards_list.append({board.board_to_json_format})
    return jsonify(boards_list)

# for testing purposes
# THIS IS KIND OF WORKING:
# the table updates with a new board
# BUGS still occur: maybe I went too far creating the relationships ahead of time.

@boards_bp.route("", methods=["POST"], strict_slashes=False)
def add_board():
    board_post_request = request.get_json()
    new_board = Board(title=board_post_request["title"],
                    owner=board_post_request["owner"])

    #TODO: validate fields!!!
    db.session.add(new_board)
    db.session.commit()

    return jsonify({"board": new_board.board_to_json_format()}), 201



# not sure about this y'all:
# @boards_bp.route("<board_id>/cards", methods=["GET"], strict_slashes=False)
# def get_cards():
#     pass

# @cards_bp.route("<board_id>/cards", methods=["POST"], strict_slashes=False)
# def add_cards():
#     pass

# The example implementation defines these endpoints.
# GET /boards (done, not tested)
# POST /boards (done, tested, updates table but has bugs)
# GET /boards/<board_id>/cards (not implemented from this one on)
# POST /boards/<board_id>/cards
# DELETE /cards/<card_id>
# PUT /cards/<card_id>/like