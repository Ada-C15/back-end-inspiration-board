
from flask import Blueprint, request, jsonify
from app import db
from app.models.card import Card
from app.models.board import Board

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
def add_board():
    response = request.get_json()
    # validate!

    new_board = Board(title=response["title"],
                    owner=response["owner"])

    db.session.add(new_board)
    db.session.commit()

    return jsonify(new_board.board_to_json()), 201


# GET /boards/<board_id>/cards
@boards_bp.route("/<board_id>/cards", methods=["GET"], strict_slashes=False)
def get_cards(board_id):
    current_board = Board.query.get(board_id) #!!???
    # needs validachon
    return jsonify(current_board.cards_list_to_json()), 200


# POST /boards/<board_id>/cards
@boards_bp.route("<board_id>/cards", methods=["POST"], strict_slashes=False)
def add_card(board_id):

    current_board = Board.query.get(board_id)
    response = request.get_json() 

    new_card = Card(
                message=response["message"],

                # should the likes_count have a default value of 0?
                # I added a default value of 0 to the card model on line 11
                # I commented out line 64 and the post request works with just the "message" in the post request 
                # likes_count=likes_count,
                board=board_id)
    
    db.session.add(new_card)

    current_board.cards.append(new_card)
    db.session.add(current_board)
    db.session.commit()

    # not sure if this is a preference, but line 74 returns a list 
    # should we return just the 1 card each post request? 
    # return jsonify(current_board.cards_list_to_json()), 201

    return jsonify(new_card.card_to_json()), 201


@boards_bp.route("<board_id>/cards/<card_id>", methods=["DELETE"], strict_slashes=False)
def delete_card(board_id, card_id):
    card_to_delete = Card.query.get(card_id)
    db.session.delete(card_to_delete)
    db.session.commit()
    return "deleted!", 200


@boards_bp.route("<board_id>/cards/<card_id>/likes", methods=["PUT"], strict_slashes=False)
def increase_likes(board_id, card_id): 

    # response = request.get_json() 
    
    current_board = Board.query.get(board_id)
    
    current_card = Card.query.get(card_id)

    if current_board.board_id == current_card.board:
        current_card.likes_count += 1
    
    db.session.add(current_card)
    db.session.commit()

    return jsonify(current_card.card_to_json()), 200
