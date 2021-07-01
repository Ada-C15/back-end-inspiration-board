from flask import current_app
from app import db
from sqlalchemy.orm import relationship, backref


class Card(db.Model):

    __tablename__ = "cards"
    card_id = db.Column(db.Integer, primary_key=True) #, autoincrement=True)
    message = db.Column(db.String) # , nullable=False)
    likes_count = db.Column(db.Integer, default=0) # , nullable=False)
    board_id = db.Column(db.Integer, db.ForeignKey('boards.board_id')) # , nullable=False) 
    # had to remove nullable constraints


    def card_to_json(self):
        card_to_json = {
            'card_id': self.card_id,
            'message': self.message,
            'likes_count': self.likes_count,
            'board_id': self.board,
        }
        return card_to_json

# T O D O: we need to implement logic or have a function to increase 'likes_count': self.likes_count,
