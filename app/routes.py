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
    

# (read) GET all the cards for a selected board 

# (create) POST a new card for a selected board by id 


#=====================================================#
#                    CARD ROUTES                      #
#=====================================================#

# DELETE a card by id 

# +1 likes feature, part of card model 
