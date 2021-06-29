from flask import Blueprint, request, jsonify, make_response
from app import db


boards_bp = Blueprint('boards', __name__, url_prefix="/boards")
cards_bp = Blueprint('cards', __name__. url_prefix="/cards")

######## BOARDS CRUD ########

# GET /boards
@boards_bp.route("", methods=["GET"])
def get_all_boards():
    pass

# POST /boards
@boards_bp.route("", methods=["POST"])
def create_new_board():
    pass

# GET /boards/{id}
@boards_bp.route("/<id>", methods=["GET"])
def get_single_board():
    pass

# DELETE /boards/id
@boards_bp.route("/<id>", methods=["DELETE"])
def delete_single_board():
    pass

# DELETE /boards 
@boards_bp.route("", methods=["DELETE"])
def delete_all_boards():
    pass

# GET /boards/{id}/cards
@boards_bp.route("/<id>/cards", methods=["GET"])
def get_cards_for_specific_board():
    pass

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