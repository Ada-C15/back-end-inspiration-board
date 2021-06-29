from flask import Blueprint, request, jsonify, make_response
from app import db
from app.models.board import Board
from app.models.card import Card

# example_bp = Blueprint('example_bp', __name__)
boards_bp = Blueprint("boards", __name__, url_prefix="/boards") 
cards_bp = Blueprint("cards", __name__, url_prefix="/cards") 


## Boards ## 

@boards_bp.route("", methods=["POST","GET"])
def handle_boards():
    if request.method == "POST":
        request_body = request.get_json()
        if 'title' in request_body and 'owner' in request_body: 
            new_board = Board(title=request_body["title"],
                            owner=request_body["owner"])
            db.session.add(new_board)
            db.session.commit()

            response = {"board":new_board.board_response()}
            return jsonify(response), 201

        else:
            return make_response ({"Invalid data error": "please include title and owner information"},400)

    elif request.method == "GET":
        boards = Board.query.all()
    
        boards_response = []
        for board in boards:
            boards_response.append(board.board_response())
        return jsonify(boards_response),200