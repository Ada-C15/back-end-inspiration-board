from flask import Blueprint, request, jsonify, make_response
from app import db

from app.models.board import Board

# example_bp = Blueprint('example_bp', __name__)
boards_bp = Blueprint("boards", __name__, url_prefix="/boards")


#=====================================================#
#                   BOARD ROUTES                      #
#=====================================================#

# (create) POST a new board
@boards_bp.route("",)

# (read) GET all the boards

# (read) GET a board by id 

#=====================================================#
#                    CARD ROUTES                      #
#=====================================================#


# (create) POST a new card for a selected board by id 
@boards_bp.route("",)

# (read) GET all the cards for a selected board 

# DELETE a card 


# +1 likes feature, part of card model 