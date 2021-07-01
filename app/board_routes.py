
from flask import Blueprint, request, jsonify
from app import db
from app.models.card import Card
from app.models.board import Board
from flask_cors import cross_origin

boards_bp = Blueprint("boards", __name__, url_prefix="/boards")

# GET /boards
@boards_bp.route("", methods=["GET"], strict_slashes=False)
def get_boards():
    all_boards = Board.query.all()
    boards_list = []
    for board in all_boards:
        boards_list.append(board.board_to_json())
    return jsonify(boards_list), 200

# GET 1 single board /boards
@boards_bp.route("/<board_id>", methods=["GET"], strict_slashes=False)
def get_one_board(board_id):
    board = Board.query.get(board_id)
    
    if board is None:
        return jsonify({"Error": f"Board {board_id} does not exist."}), 404
    else:
        return jsonify(board.board_to_json()), 200

# POST /boards
@boards_bp.route("", methods=["POST"], strict_slashes=False)
@cross_origin
def add_board():
    response = request.get_json()
    # validate!

    new_board = Board(title=response["title"],
                    owner=response["owner"])

    db.session.add(new_board)
    db.session.commit()

    return jsonify(new_board.board_to_json()), 201

# Delete a single board 
# @boards_bp.route("<board_id>/", methods=["DELETE"], strict_slashes=False)
# def delete_board(board_id):
#     board_to_delete = Board.query.get(board)
#     db.session.delete(board_to_delete)
#     db.session.commit()
#     return "deleted!", 200



