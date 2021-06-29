from app import db
from flask import current_app


class Card(db.Model):
    card_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    message = db.Column(db.String)
    likes_count = db.Column(db.Integer)
    board_id = db.Column(db.Integer, db.ForeignKey('board.board_id'), nullable=True)


    # set default like count to 0 
    # autoincrement = True? -> it should go up by 1, could do this in the routes? 
