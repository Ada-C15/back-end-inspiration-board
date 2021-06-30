from flask import Blueprint, request, jsonify, make_response
from app import db

from app.models.board import Board
from app.models.card import Card
import requests
import os

# example_bp = Blueprint('example_bp', __name__)
boards_bp = Blueprint("boards", __name__, url_prefix="/boards")
# cards_bp = Blueprint("cards", __name__, url_prefix="/cards")

#=====================================================#
#                   BOARD ROUTES                      #
#=====================================================#

# (read) GET all the boards
@boards_bp.route("", methods=["GET"], strict_slashes=False)
def list_all_boards():
    """
    Get all Boards 
    """
    boards = Board.query.all()

    boards_response = [board.to_json() for board in boards]

    return jsonify(boards_response), 200

# (create) POST a new board
@boards_bp.route("", methods=["POST"])
def add_new_board(): 
    """
    Create a new Board
    """
    request_body = request.get_json()

    try:
        request_body["title"]
        request_body["owner"]
    except:
        return jsonify({
            "details": "Invalid data"
        }), 400

    new_board = Board(
            title=request_body["title"],
            owner=request_body["owner"]
            )
    
    db.session.add(new_board)
    db.session.commit()

    return make_response(new_board.to_json(), 201)


# (create) POST a new card for a selected board by id 

# def create_goal():
#     request_body = request.get_json()
#     if "title" in request_body:
#         new_goal = Goal(
#             title=request_body["title"])
#         db.session.add(new_goal)
#         db.session.commit()
#         return jsonify({"goal": new_goal.to_dict()}), 201

#     new_goal = make_response({"details": "Invalid data"}, 400)

# @boards_bp.route("/<board_id>/cards", methods=["POST"], strict_slashes=False)
# def add_cards_to_goal(board_id):

#     request_body = request.get_json()
#     tasks = request_body["task_ids"]
#     # (db)
#     goal = Goal.query.get(goal_id)
#     for task_id in tasks:
#         task_db_object = Task.query.get(task_id)
#         goal.tasks.append(task_db_object)
#         # task_db_object.goal_id = int(goal_id)
#         db.session.commit()
#     return {"id": goal.goal_id,
#             "task_ids": tasks}, 200



# (read) GET all the cards for a selected board 

@boards_bp.route("/<board_id>/cards", methods=["GET"], strict_slashes=False)
def get_cards_of_one_board(board_id):
    board = Board.query.get_or_404(board_id)
    board_response = board.to_json()
    board_response["cards"] = [card.to_json() for card in board.cards]
    return jsonify(board_response), 200




#=====================================================#
#                    CARD ROUTES                      #
#=====================================================#

# DELETE a card by id 

# +1 likes feature, part of card model 
