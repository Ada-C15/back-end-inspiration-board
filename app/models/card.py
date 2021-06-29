from app import db
from sqlalchemy.orm import relationship
from flask import current_app

class Card(db.Model):
    card_id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String)
    likes_count = db.Column(db.Integer)
    
    board_id = db.Column(db.Integer, db.ForeignKey('board.board_id'))
    board = db.relationship("Board", back_populates="card", lazy=True)


    def card_json(self):
        return {
            "id": self.card_id,
            "message": self.message,
            "likes_count": self.likes_count
        }