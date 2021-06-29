from flask import Blueprint, request, jsonify, make_response
from app import db
from app.models.board import Board
from app.models.card import Card

# example_bp = Blueprint('example_bp', __name__)

card_bp = Blueprint("cards", __name__, url_prefix="/cards")
board_bp = Blueprint("boards", __name__, url_prefix="/boards")

###################### Part A: GET /boards endpoint ##################
# a. 
# GET /boards 
# Request: board id;
# Response:  {“board_id”, “title”, “owner”}
@board_bp.route("", methods=["GET"])
def board():
    boards = Board.query.all()
    board_response = []

    for board in boards: 
        board_response.append(board.to_json())

    return jsonify(board_response), 200

###################### Part B: POST /boards endpoint ##################
#b
# #b. POST /boards
# Request: title, owner
# Response:  update db && success code ?  

@board_bp.route("", methods=["POST"])
def create_board():
    request_body = request.get_json()

    try: 
        create_board = Board(title=request_body["title"],
                            owner=request_body["owner"])
    except KeyError:
        return make_response({
            "details": "Invalid data"
        }, 400)
    db.session.add(create_board)
    db.session.commit()
    return {
        "board": create_board.to_json()
    }, 201

###################### Part C & D: "GET", "POST" /boards/<board_id>/cards endpoint ##################
# c. GET /boards/<board_id>/cards
# Request: board_id 
# Response:  {“card_id”, “message”, “likes_count”, “board_id”}

# d. POST /boards/<board_id>/cards
# Request: board_id
# Response:  update db && success code ?

@board_bp.route("/<int:id>/cards", methods=["GET", "POST"])
def board_cards(id):
    board = Board.query.get(id)
    if not board:
        return make_response('Board doesn\'t exist', 404)

    if request.method == 'POST':
        card_ids = request.get_json()['card_ids']
        for card_id in card_ids:
            card = Card.query.get(card_id)
            if card not in board.cards:
                board.cards.append(card)
        response_body = {
            'id': board.id,
            'card_ids': [card.card_id for card in board.cards]
        }
        db.session.commit()
        return jsonify(response_body), 200

    cards = []
    for card in board.cards:
        card_json = {
            'id': card.card_id,
            'message': card.message,
            'like_count': card.like_count,
            'is_complete': bool(card.completed_at)
        }
        card.append(card_json)

    response_body = {
        'id': board.id,
        'title': board.title,
        'owner': board.owner
    }

    return jsonify(response_body), 200

###################### Part E: DELETE  /cards/<card_id> endpoint ##################
# e. DELETE /cards/<card_id>
# Request: card_id
# Response:  successfully delete message ?

@card_bp.route("/<int:id>", methods=["DELETE"])
def delete_card(id):
    card = Card.query.get(id)
    if card == None:
        return make_response(f"Card {id} not found", 404)
    db.session.delete(card)
    db.session.commit()
    return make_response({"details": f"Card {id} \"{card.title}\" successfully deleted"}, 200)



###################### Part F: PUT  /cards/<card_id>/like endpoint ##################
# f. PUT /cards/<card_id>/like
# Request: card_id
# Response:  update db && success code ? 

@card_bp.route("/<int:id>/like", methods=["PUT"])
def update_card(id):
    card = Card.query.get(id)
    if not card:
        return make_response('Goal not found.', 404)
    request_body = request.get_json()
    card.title = request_body['title']
    db.session.commit()
    return jsonify({'card': card.to_json()}), 200
