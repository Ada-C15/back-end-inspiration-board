from flask import Blueprint, request, jsonify, make_response
from app import db
from app.models.board import Board
from app.models.card import Card

# example_bp = Blueprint('example_bp', __name__)




board_bp = Blueprint("boards",__name__,url_prefix="/boards")
card_bp = Blueprint("cards", __name__, url_prefix="/cards")

@board_bp.route("", methods=["POST"])

def create_a_board(): 
    request_body = request.get_json()

    for board_attribute in ["title","owner"]:
        if board_attribute not in request_body:
            return jsonify(f'Missing required: {board_attribute}'),400


    new_board = Board.from_dict(request_body)
  

    db.session.add(new_board)
    db.session.commit()



    response = jsonify (new_board.as_json())
    return make_response(response, 201)


@board_bp.route("", methods=["GET"])
def retrieve_all_boards():

    boards = Board.query.all()

    if boards is None:
        return make_response("",200)
    else:
        response = [board.as_json() for board in boards]
        return make_response(jsonify(response), 200)



@board_bp.route("/<board_id>", methods=["GET"])
def retrieve_one_board(board_id):
    board = Board.query.filter_by(board_id = board_id).first()

    if board is None:
        return make_response("", 404)


    if request.method == "GET":
        return jsonify(board.as_json())




@board_bp.route("/<board_id>/cards", methods=["GET", "POST"])
def retrieve_all_cards(board_id):
    cards = Card.query.filter_by(board_id=board_id).all()

    if request.method == "GET":

        if cards is None:
            return make_response("",200)
        else:
            response = [card.as_json() for card in cards]
            return make_response(jsonify(response), 200)


    elif request.method == "POST": 

        board = Board.query.filter_by(board_id = board_id).first()
        request_body = request.get_json()
        for card_attribute in ["message"]:
            if card_attribute not in request_body:
                return jsonify(f'Missing required: {card_attribute}'),400
        if len(request_body["message"]) > 40:
            return jsonify(f'Message too long'),400

        if request_body["message"] == "":
            return jsonify(f'Message empty, please enter a valid message'), 400

        
    # new_card= Card.from_dict(request_body)
        new_card = Card(message=request_body["message"],board_id=board_id)
   
        db.session.add(new_card)
        db.session.commit()

        response = new_card.as_json()
        return make_response(jsonify(response), 201)




@card_bp.route("/<card_id>", methods=["DELETE"])
def delete_existing_card(card_id):
    card = Card.query.filter_by(card_id=card_id).first()

    if card is None:
        return make_response("", 404)

    db.session.delete(card)
    db.session.commit()
    return jsonify (
        {
            "id": card_id
        })


@card_bp.route("/<card_id>", methods=["PATCH"])
def add_like_to_single_card(card_id):
    card = Card.query.filter_by(card_id=card_id).first()

    if card is None:
        return make_response("", 404)

    card.likes_count += 1
    db.session.commit()
    return jsonify (card.as_json())

