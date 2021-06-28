from flask import Blueprint, request, jsonify, make_response
from app.models.card import Card
from app.models.board import Board
from app import db

# example_bp = Blueprint('example_bp', __name__)
# Boards BP
boards_bp = Blueprint("boards", __name__, url_prefix="/boards")

'''
Start with making the conventional endpoints for:
Getting a list of all boards
Creating a board
'''

# Get all boards
@boards_bp.route("", methods=["GET"])
def get_all_boards():
    boards = Board.query.all()
    boards_list = []
    for board in boards:
        # What do we want the response to include?
        # This implementation throws a 'Board is not subscriptable' error. 
        boards_list.append(board["title"])
    sorted_boards_list = sorted(boards_list, key = lambda i: i['id'])
    return jsonify(sorted_boards_list), 200

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