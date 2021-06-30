from flask import Blueprint, request, jsonify, make_response
from app import db
from .models.board import Board
from .models.card import Card

boards_bp = Blueprint("board", __name__, url_prefix="/boards")

# route working
@boards_bp.route("", methods=["GET"], strict_slashes=False)
def boards():
    if request.method == "GET":
        board_list = Board.query.all()

        boards_response = []

        for board in board_list: 
            boards_response.append(board.board_to_json())
        return jsonify(boards_response)

# route working
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
        return {"board": new_board.board_to_json()}, 201

# route working
@boards_bp.route("<board_id>/cards", methods=["POST"], strict_slashes=False) 
# post card to one board
def post_board_card(board_id):

    board = Board.query.get(board_id) # get correct board using id passed into endpoint

    if board is None: # if board doesn't exist, return error
        return "", 404

    request_body = request.get_json() # deviated from Task List API logic here
    
    new_card = Card(message = request_body["message"],
                    likes_count = request_body["likes_count"],
                    board_id = board_id) # creates id here, reduces code
                    # this is going to have to become logic

    #new_card.board_id = board_id # assign board id to new instance of/row in Card
    db.session.add(new_card)
    db.session.commit()
    return {"card": new_card.card_to_json()}, 201

    # return {
    #     "board_id": board.board_id,
    #     "card_id": new_card.card_id # we might be returning something else here
    # }

# route working 
@boards_bp.route("<board_id>/cards", methods=["GET"], strict_slashes=False) # get all cards for specific board
# get cards of one board
def get_board_cards(board_id):
    board = Board.query.get(board_id) # get correct board using id passed into endpoint

    if board is None: # if board doesn't exist, return error
        return "", 404
        
    associated_cards = Card.query.filter_by(board_id=board_id)

    list_of_cards = []

    for card in associated_cards:
        list_of_cards.append(card.card_to_json())

    return {"cards": list_of_cards}, 200

    # return {
    #     "board_id": board.board_id, # board data was obtained on line 29
    #     "board_title": board.title,
    #     "cards": list_of_cards
    #     }


cards_bp = Blueprint("cards", __name__, url_prefix="/cards")

@cards_bp.route("/<card_id>", methods=["DELETE"], strict_slashes=False)
def cards(card_id):

    card = Card.query.get(card_id)

    if card is None:
        return "", 404

    db.session.delete(card)
    db.session.commit()

    return jsonify({
        "details": f'Card {card.card_id} "{card.title}" successfully deleted.'
    }) 



