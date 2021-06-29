from flask import Blueprint, request, jsonify, make_response
from app import db
from .models.board import Board

board_bp = Blueprint("boards", __name__, url_prefix="/boards")

@board_bp.route("", methods=["POST"], strict_slashes=False)
def create_board():
    request_body=request.get_json()
    if "title" in request_body and "owner" in request_body:
        new_board = Board(title= request_body["title"],
                            owner= request_body["owner"])
        db.session.add(new_board)
        db.session.commit()

        return