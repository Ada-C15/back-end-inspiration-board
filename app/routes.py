from flask import Blueprint, request, jsonify, make_response
from app import db
from app.models.board import Board
from app.models.card import Card


boards_bp = Blueprint('boards', __name__, url_prefix="/boards")
cards_bp = Blueprint('cards', __name__, url_prefix="/cards")

######## BOARDS CRUD ########

# GET /boards
@boards_bp.route("", methods=["GET"])
def get_all_boards():
    boards = Board.query.all()
    return jsonify([board.to_json() for board in boards])

# POST /boards
@boards_bp.route("", methods=["POST"])
def create_new_board():
    request_body = request.get_json()
    try:
        new_board = Board(title=request_body['title'],
                            owner=request_body['owner'])
    except KeyError:
        return make_response({
            "details": "invalid data"
        }, 400)
    db.session.add(new_board)
    db.session.commit()
    response = {
        "board": new_board.to_json()
    }
    return make_response(jsonify(response), 201)

# GET /boards/{id}
@boards_bp.route("/<id>", methods=["GET"])
def get_single_board(id):
    board = Board.query.get(id)
    if board is None:
        return make_response("", 404)

    return {
        "board": board.to_json()
    }
    

# DELETE /boards/id
@boards_bp.route("/<id>", methods=["DELETE"])
def delete_single_board(id):
    board = Board.query.get(id)
    if board is None:
        return make_response("", 404)
    db.session.delete(board)
    db.session.commit()
    return {
        "details": f"Board {board.board_id} \"{board.title}\" successfully deleted"
    }

# DELETE /boards 
@boards_bp.route("", methods=["DELETE"])
def delete_all_boards():
    boards = Board.query.all()
    db.session.delete(boards)
    db.session.commit()
    return {
        "details": "Boards successfully deleted"
    }## might not work, might need for loop

# GET /boards/{id}/cards
@boards_bp.route("/<id>/cards", methods=["GET"])
def get_cards_for_specific_board(id):
    board = Board.query.get(id)
    if board is None:
        return make_response("", 404)

    associated_cards = Card.query.filter_by(board_id=int(id))

    response = board.to_json()
    response['cards'] = [card.to_json() for card in associated_cards]

    return response

# POST /boards/id/cards
@boards_bp.route("/<id>/cards", methods=["POST"])
def create_new_card():
    pass


######## CARDS CRUD #########

# GET /cards/{id}
@cards_bp.route("/cards/<id>", methods=["GET"])
def get_single_card():
    pass

# PATCH /card/{id}/like
@cards_bp.route("/cards/<id>/like", methods=["PATCH"]) #*** simon used a PUT for this
def like_card():
    pass

# DELETE /cards/{id}
@cards_bp.route("/cards/<id>", methods=["DELETE"])
def delete_card():
    pass



######### EXTRAS ##########
# PUT /board/{id} < unnecessary, extra feature?
# PUT /cards/{id} < unnecessary