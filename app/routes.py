from flask import Blueprint, request, jsonify, make_response
from app.models.card import Card
from app.models.board import Board
from app import db

# example_bp = Blueprint('example_bp', __name__)
# Boards BP
boards_bp = Blueprint("boards", __name__, url_prefix="/customers")

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
        # 
        boards_list.append(board)
    sorted_boards_list = sorted(boards_list, key = lambda i: i['id'])
    return jsonify(sorted_boards_list), 200