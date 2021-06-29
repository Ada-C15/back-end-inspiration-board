from app import db
from flask import current_app

class Board(db.Model):
    __tablename__="board"
    board_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    owner = db.Column(db.String)
    card_id = db.Column(db.Integer, db.ForeignKey('card.card_id'), nullable=True)
