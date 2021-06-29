from flask import Blueprint, request, jsonify, make_response
from app import db

card_bp = Blueprint('card', __name__, url_prefix="/boards")
