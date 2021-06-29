'''
  Boards Routes
  - all boards => GET, POST
  - single board => GET, PUT, DELETE
'''

from flask import Blueprint, request, jsonify, make_response
from app import db
from app.models.board import Board

# example_bp = Blueprint('example_bp', __name__)
boards_bp = Blueprint('board', __name__, url_prefix='/boards')

# ==============================================================
# ===== All Boards =====
# ==============================================================

@boards_bp.route("", methods=["GET"], strict_slashes=False)
def get_boards():
  boards = Board.query.all()
  return make_response({'boards_list' : [board.to_dict() for board in boards]}, 200)
  # returns a json with a single key, the value is a list of all the boards info (id, title, owner, and list of cards)

@boards_bp.route("", methods=["POST"], strict_slashes=False)
def post_boards():
  request_body = request.get_json()

  try:
    new_board = Board(
      title=request_body["title"],
      owner=request_body["owner"]
    )
  except KeyError:
    return make_response({'details' : 'Missing data'}, 400)

  db.session.add(new_board)
  db.session.commit()

  return make_response(new_board.to_dict(), 201)
  # returns all the info about the new board, including it's assigned id, no cards yet


# ==============================================================
# ===== Single Board =====
# ==============================================================

@boards_bp.route("/<board_id>", methods=["GET"], strict_slashes=False)
def get_board(board_id):
  board = Board.query.get_or_404(board_id)
  return make_response(board.to_dict(), 200)
  # returns json with id, title, owner, cards list


@boards_bp.route("/<board_id>", methods=["PUT"], strict_slashes=False)
def put_board(board_id):
  board = Board.query.get_or_404(board_id)
  request_body = request.get_json()

  try:
    board.title=request_body["title"],
    board.owner=request_body["owner"]
  except KeyError:
    return make_response({'details' : 'Missing data'}, 400)

  db.session.commit()
  return make_response(board.to_dict(), 200)
  # returns json with id, title, owner, cards list

@boards_bp.route("/<board_id>", methods=["DELETE"], strict_slashes=False)
def delete_board(board_id):
  board = Board.query.get_or_404(board_id)
  db.session.delete(board)
  db.session.commit()
  return make_response({'id' : board_id}, 200)
  # returns the id of the deleted board


# ==============================================================
# ===== Helper Functions =====
# ==============================================================
