from flask import Blueprint, request, jsonify, make_response
from app import db
from .models.board import Board
from .models.card import Card
from flask import request, Blueprint, make_response, jsonify



boards_bp = Blueprint("board", __name__, url_prefix="/boards")

@boards_bp.route("", methods=["GET"], strict_slashes=False)
def boards():
    if request.method == "GET":
        board_list = []

        for board in board_list: 
            board_list.append({
                "id": board.board_id,
                "title": board.title,
                "owner": board.owner,
                
            })
            
        return jsonify(board_list)

@boards_bp.route("", methods=["POST"], strict_slashes=False)
def create_board():
    request_body = request.get_json()
    
    if ("title" not in request_body or "owner" not in request_body):
        return jsonify({"details":"Invalid data"}),400
    
    else:
        new_board = Board(title = request_body["title"],
                        owner = request_body["owner"])

        db.session.add(new_board)
        db.session.commit()
        return (jsonify(new_board), 201)