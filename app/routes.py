from flask import Blueprint, request, jsonify, make_response
from app.models.card import Card
from app.models.board import Board
from app import db

boards_bp = Blueprint("boards", __name__, url_prefix="/boards")
cards_bp = Blueprint("cards", __name__, url_prefix="/cards")

# Get all boards


@boards_bp.route("", methods=["GET"])
def get_all_boards():
    query = Board.query.order_by(Board.board_id.asc())

    boards_list = []
    for board in query:
        boards_list.append(board.get_resp())

    return jsonify(boards_list), 200

# Create a board


@boards_bp.route("", methods=["POST"])
def create_board():
    request_body = request.get_json()

    if not ("title" in request_body and "owner" in request_body):
        return make_response({
            "error": True,
            "message": f"Invalid request body."}, 400)

    new_board = Board(
        title=request_body["title"],
        owner=request_body["owner"]
    )
    db.session.add(new_board)
    db.session.commit()
    # What does front end need as return?
    return (jsonify(f"Posted new board {new_board.title}!"), 201)


'''
Next: Create, Read, and Delete Cards
'''
# Gets all cards


@cards_bp.route("", methods=["GET"])
def get_all_card():
    query = Card.query.order_by(Card.card_id.asc())
    cards_list = []
    for card in query:
        cards_list.append(card.get_resp())
    return jsonify(cards_list), 200

# Get all cards associated with board


@boards_bp.route("/<board_id>/cards", methods=["GET"])
def get_cards(board_id):
    board = Board.query.get_or_404(
        board_id,
        description={
            "error": True,
            "message": "Board does not exist."})

    cards = Card.query.filter_by(board_id=board_id)

    cards_list = []
    for card in cards:
        cards_list.append(card.get_resp())

    return (jsonify(cards_list), 201)

# Create a card for a board


# @cards_bp.route("/<board_id>", methods=["POST"])
@boards_bp.route("/<board_id>/cards", methods=["POST"])
def create_card(board_id):

    board = Board.query.get_or_404(
        board_id,
        description={
            "error": True,
            "message": "Board does not exist."})

    request_body = request.get_json()

    if not ("message" in request_body):
        return make_response({
            "error": True,
            "message": f"Invalid request body."}, 400)

    new_card = Card(
        message=request_body["message"],
        board_id=board_id
    )
    db.session.add(new_card)
    db.session.commit()
    return (jsonify(f"Posted new card on board {new_card.board_id}!"), 201)


# # Delete a card
# DELETE /cards/<card_id>
@cards_bp.route("/<card_id>", methods=["DELETE"])
def delete_card(card_id):
    card = Card.query.get_or_404(
        card_id,
        description={
            "error": True,
            "error": f"Card with id {card_id} does not exist."})

    db.session.delete(card)
    db.session.commit()

    return ({"details": f"Card {card_id} successfully deleted."}, 200)


@cards_bp.route("/<card_id>/like", methods=["PATCH"])
def update_card_like(card_id):
    """
    Update likes (+1) for a card with specific id.
    PUT /cards/<card_id>/like
    """
    card = Card.query.get_or_404(
        card_id,
        description={
            "error": True,
            "message": f"Card with id {card_id} does not exist."})
    card.update_likes()
    db.session.commit()
    return make_response(card.get_resp(), 200)
    # return ({"details": f"Card {card_id} likes successfully updated by
    # +1."}, 200)
