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

            response = new_board.board_response()
            return jsonify(response), 201

        else:
            return make_response ("Invalid data error: please include title and owner information",400)

    elif request.method == "GET":
        boards = Board.query.all()
    
        boards_response = []
        for board in boards:
            boards_response.append(board.board_response())
        return jsonify(boards_response),200


@boards_bp.route("/<board_id>", methods=["GET","PUT","DELETE"])
def handle_a_board(board_id):
    board = Board.query.get(board_id)
    if board is None:
        return make_response ("Invadlid Board ID",404)

    elif request.method == "GET":
        response = board.board_response()
        return jsonify(response), 200

    elif request.method == "PUT":      
        form_data = request.get_json()
        board.title = form_data["title"]
        board.owner = form_data["owner"]

        db.session.commit()
        
        response = board.board_response()
        return jsonify(response), 200
        
    elif request.method == "DELETE":
        db.session.delete(board)
        db.session.commit()
        response = f"Board #{board.board_id} {board.title} successfully deleted"
        return jsonify(response), 200


## Cards ## 
@cards_bp.route("", methods=["POST","GET"])
def handle_cards():
    if request.method == "POST":
        request_body = request.get_json()
        if 'message' in request_body: 
            new_card = Card(message=request_body["message"])
            db.session.add(new_card)
            db.session.commit()

            response = new_card.card_response()
            return jsonify(response), 201

        else:
            return make_response ("Invalid data error: please include title and owner information",400)

    elif request.method == "GET":
        cards = Card.query.all()
    
        cards_response = []
        for card in cards:
            cards_response.append(card.card_response())
        return jsonify(cards_response),200


@cards_bp.route("/<card_id>", methods=["GET","PUT","DELETE"])
def handle_a_card(card_id):
    card = Card.query.get(card_id)
    if card is None:
        return make_response ("Invadlid Card ID",404)

    elif request.method == "GET":
        response = card.card_response()
        return jsonify(response), 200

    elif request.method == "PUT":      
        form_data = request.get_json()
        card.message = form_data["message"]
        card.likes_count = form_data["likes_count"]

        db.session.commit()
        
        response = card.card_response()
        return jsonify(response), 200
        
    elif request.method == "DELETE":
        db.session.delete(card)
        db.session.commit()
        response = f"Card #{card.card_id} successfully deleted"
        return jsonify(response), 200


@cards_bp.route("/<card_id>/like", methods=["PUT","GET"])
def handle_a_card_like(card_id):
    card = Card.query.get(card_id)
    if card is None:
        return make_response ("Invadlid Card ID",404)
    
    elif request.method == "GET":
        response = card.card_response()
        return jsonify(response["likes_count"]), 200

    elif request.method == "PUT":      
        form_data = request.get_json()
        card.likes_count = form_data["likes_count"]

        db.session.commit()
        response = card.card_response()
        return jsonify(response["likes_count"]), 200
