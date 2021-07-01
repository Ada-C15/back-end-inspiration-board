from flask import Blueprint, request, jsonify, make_response
from app import db
from app.models.board import Board
from app.models.card import Card


boards_bp = Blueprint('boards', __name__, url_prefix="/boards")
cards_bp = Blueprint('cards', __name__, url_prefix="/cards")


############################################## BOARDS CRUD ##########################################################


@boards_bp.route("", methods=["GET"])
def get_all_boards():
    """
    Request body: None. Accommodates query parameters in route path to sort by title or owner, or filter results by title or owner.
    Action: Gets all boards within query parameters, otherwise gets all boards in database.
    Response: A JSON list of dictionaries, each dictionary representing a board. These dictionaries contain keys "id", "title", and "owner"
    """
    sort_by_title_query = request.args.get("sort_by_title")
    sort_by_owner_query = request.args.get("sort_by_owner")
    filter_by_title_query = request.args.get("filter_by_title")
    filter_by_owner_query = request.args.get("filter_by_owner")

    if sort_by_title_query == "asc":
        boards = Board.query.order_by("title")
    elif sort_by_title_query == "desc":
        boards = Board.query.order_by(desc("title"))
    elif sort_by_owner_query == "asc":
        boards = Board.query.order_by("owner")
    elif sort_by_owner_query == "desc":
        boards = Board.query.order_by(desc("owner"))
    elif filter_by_title_query:
        boards = Board.query.filter_by(title=filter_by_title_query)
    elif filter_by_owner_query:
        boards = Board.query.filter_by(owner=filter_by_owner_query)
    else:
        boards = Board.query.all()

    return jsonify([board.to_json() for board in boards])


@boards_bp.route("", methods=["POST"])
def create_new_board():
    """
    Request body: A JSON dictionary with "title" and "owner"
    Action: Creates a new board with specified title and owner. If either of these details is missing from request body, throws a 400 error.
    Response: 201 Created. Returns a JSON dictionary with key "board", whose value is another dictionary detailing new board's info ("board_id", "title", "owner")
    """
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


@boards_bp.route("/<id>", methods=["GET"])
def get_single_board(id):
    """
    Request body: None; requested board id specified in route path.
    Action: Gets baord with specified ID; returns 404 response if no board found.
    Response: 200 OK, returns JSON dictionary with key "board" whose value is another dictionary detailing the board's info ("board_id", "title", "owner")
    """
    board = Board.query.get(id)
    if board is None:
        return make_response("", 404)

    return {
        "board": board.to_json()
    }
    


@boards_bp.route("/<id>", methods=["DELETE"])
def delete_single_board(id):
    """
    Request body: None. Requested board id is specified in route path.
    Action: Deletes board at specified ID if board exists.
    Response: 404 if not found; otherwise, 200 OK. Returns dictionary with message that the selected board was deleted.
    """
    board = Board.query.get(id)
    if board is None:
        return make_response("", 404)
    db.session.delete(board)
    db.session.commit()
    return {
        "details": f"Board {board.board_id} \"{board.title}\" successfully deleted"
    } ### Also not in the hints doc


@boards_bp.route("", methods=["DELETE"])
def delete_all_boards():
    """
    Request body: None. Query parameters optionally provided in route path to delete boards by title or owner.
    Action: Deletes all boards if no query parameters. Query parameters accommodates deleting all boards that match specific title or owner.
    Response: 404 if empty database or invalid owner/title query param. Otherwise, 200 ok. Returns message confirming board deletion.
    """
    filter_by_title_query = request.args.get("filter_by_title")
    filter_by_owner_query = request.args.get("filter_by_owner")

    if filter_by_title_query:
        boards = Board.query.filter_by(title=filter_by_title_query)
    elif filter_by_owner_query:
        boards = Board.query.filter_by(owner=filter_by_owner_query)
    else:
        boards = Board.query.all()

    if len(boards) == 0:
        return make_response("", 404)

    for board in boards:
        db.session.delete(board)
    db.session.commit()
    return {
        "details": "Boards successfully deleted"
    }


@boards_bp.route("/<id>/cards", methods=["GET"])
def get_cards_for_specific_board(id):
    """
    Request body: None. Optional query parameter to sort by like count, ascending or descending.
    Action: Gets all cards associated with the baord id provided in route path.
    Response: 200 OK. 404 if board not found. Returns JSON list of dictionaries representing resulting cards.
    """
    sort_query = request.args.get("sort")

    board = Board.query.get(id)
    if board is None:
        return make_response("", 404)

    if sort_query == "likes":
        associated_cards = Card.query.filter_by(board_id=int(id)).order_by(desc("likes_count"))
    elif sort_query == "id":
        associated_cards = Card.query.filter_by(board_id=int(id)).order_by("id")
    elif sort_query == "alphabetical":
        associated_cards = Card.query.filter_by(board_id=int(id)).order_by("message")
    else:
        associated_cards = Card.query.filter_by(board_id=int(id))

    return jsonify([card.to_json() for card in associated_cards])


@boards_bp.route("/<id>/cards", methods=["POST"])
def create_new_card(id):
    """
    Request body: A JSON dictionary with a single key-value pair ("message": <message_body>)
    Action: Creates a new entry in cards table with default (0) like_count, message provided in request body,
    and board id provided in route.
    Response: 201 Created; response body is JSON dictionary with keys "card_id", "message", "likes_count", and "board_id"
    """
    board = Board.query.get(id)
    if board is None:
        return make_response("", 404)
    
    request_body = request.get_json()

    try:
        note = request_body['message']
        if len(note) > 40:
            return make_response ({
                "details": "message exceeds 40 characters"
            }, 400)
        new_card = Card(message=request_body['message'],
                            board_id=id)
    except KeyError:
        return make_response({
            "details": "invalid data"
        }, 400)

    db.session.add(new_card)
    db.session.commit()

    response = {
        "card": new_card.to_json()
    }

    return make_response(jsonify(response), 201)



############################################## CARDS CRUD ##########################################################
#GET /cards/ all
@cards_bp.route("", methods=["GET"])
def get_all_cards():
    cards = Card.query.all()
    return jsonify([card.to_json() for card in cards])


# GET /cards/{id}
@cards_bp.route("/<id>", methods=["GET"])
def get_single_card(id):
    card = Card.query.get(id)
    if card is None:
        return make_response("", 404)

    return {
        "card": card.to_json()
    } #### not in the hints doc 


# PATCH /card/{id}/like
@cards_bp.route("/<id>/like", methods=["PATCH"]) #*** simon used a PUT for this
def like_card(id):
    """
    Request body: none
    Action: Increases likes_count by 1 if card exists and updates database
    Response: A JSON dictionary with key "card", whose value is another dictionary detailing updated card info,
    with keys "card_id", "message", "likes_count", and "board_id"
    """
    card = Card.query.get(id)
    if card is None:
        return make_response("", 404)

    card.likes_count += 1

    db.session.commit()

    return {
        "card": card.to_json()
    }


# DELETE /cards/{id}
@cards_bp.route("/<id>", methods=["DELETE"])
def delete_card(id):
    card = Card.query.get(id)
    if card is None:
        return make_response("", 404)
    db.session.delete(card)
    db.session.commit()
    return {
        "details": f"Card {card.card_id} \"{card.message}\" successfully deleted"
    }



######### EXTRAS ##########
# PUT /board/{id} < unnecessary, extra feature?
# PUT /cards/{id} < unnecessary

# GET /boards/<owner> (get boards by owner) or query param
# DELETE /boards/<owner> (delete boards that have a specific owner) or query param
