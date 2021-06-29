from flask import Blueprint, request, jsonify, make_response
from app import db
from app.models.card import Card
from dotenv import load_dotenv

load_dotenv()

# example_bp = Blueprint('example_bp', __name__)
cards_bp = Blueprint("cards", __name__, url_prefix="cards")


# ***************************** CARD ROUTES ***********************

@cards_bp.route("/<board_id>", methods=["POST"], strict_slashes=False)
def post_card():
    request_body = request.get_json()
    new_card = Card(message= request_body["message"])
    
    if new_card["message"] == "" \
        or type(new_card["message"]) is not str:
        return 404
    else:
        db.session.add(new_card)
        db.session.commit()
        return make_response

    #create model method to return data