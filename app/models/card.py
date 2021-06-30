from app import db
from flask import current_app


class Card(db.Model):
    card_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    message = db.Column(db.String)
    likes_count = db.Column(db.Integer, default=0)
    board_id = db.Column(db.Integer, db.ForeignKey('board.board_id'), nullable=True)

    def to_json(self): 
        return {  
            "card_id": self.card_id,   
            "message": self.message,
            "likes_count": self.likes_count,
            "board_id": self.board_id
        }
    # set default like count to 0 
    # autoincrement = True? -> it should go up by 1, could do this in the routes? 
