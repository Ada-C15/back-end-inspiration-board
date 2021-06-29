'''
  Boards Routes
  - all boards => GET, POST
  - single board => GET, PUT, DELETE
'''

from flask import Blueprint, request, jsonify, make_response
from app import db

# example_bp = Blueprint('example_bp', __name__)
boards_bp = Blueprint('board', __name__, url_prefix='/boards')

# ==============================================================
# ===== All Boards =====
# ==============================================================

@boards_bp.route("", methods=["GET"], strict_slashes=False)
def get_boards():
  pass

@boards_bp.route("", methods=["POST"], strict_slashes=False)
def post_boards():
  pass


# ==============================================================
# ===== Single Board =====
# ==============================================================

@boards_bp.route("/<board_id>", methods=["GET"], strict_slashes=False)
def get_board():
  pass

@boards_bp.route("/<board_id>", methods=["PUT"], strict_slashes=False)
def put_board():
  pass

@boards_bp.route("/<board_id>", methods=["DELETE"], strict_slashes=False)
def delete_board():
  pass


# ==============================================================
# ===== Helper Functions =====
# ==============================================================
