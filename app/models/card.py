from flask import current_app

from app import db

class Card(db.Model):
    card_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    message = db.Column(db.String)
    likes_count = db.Column(db.Integer)
    color = db.Column(db.String, default=None)
    board_id = db.Column(db.Integer, db.ForeignKey('board.board_id'))

    def to_dict(self):
        return {
            "id": self.card_id,
            "message": self.message,
            "likes_count": self.likes_count,
            "color": self.color,
            "board_id": self.board_id
        }