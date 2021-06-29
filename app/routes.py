from flask import Blueprint, request, jsonify, make_response
from app import db


boards_bp = Blueprint('boards', __name__, url_prefix="/boards")
cards_bp = Blueprint('cards', __name__. url_prefix="/cards")

######## BOARDS CRUD ########

# GET /boards
# POST /boards
# GET /boards/{id}
# PUT /board/{id} < unnecessay
# DELETE /boards/id
# DELETE /boards 
# GET /boards/{id}/cards

######## CARDS CRUD #########

# GET /cards
# POST /cards ***
# GET /cards/{id}
# PUT /card/{id}/like
# PUT /cards/{id} < unnecessary
# DELETE /cards/{id}