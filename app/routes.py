from flask import Blueprint, request, jsonify, make_response
from app import db
from app.models.board import Board
from app.models.card import Card
import requests

# example_bp = Blueprint('example_bp', __name__)

