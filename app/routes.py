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
