# from flask import current_app
from app import db


# Card, table name: card
# card_id, int, primary key
# message, string
# likes_count, int

class Card(db.Model):
    card_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    message = db.Column(db.String, nullable=False)
    likes_count = db.Column(db.Integer, nullable=False) # autoincrement=True?
    # board = db.Column(db.Integer, db.ForeignKey('board.board_id')) # nullable=False?
    # creating these tables with no relationship as of now, following instructions



# just in case like Board:
#
# def card_to_json_format(self):
#     card_to_json = {
#         "id": self.task_id,
#         "message": self.title,
#         "likes_count": self.description,
#     }
#     if self.board is not None:
#         card_to_json["board_id"] = self.board
#     return card_to_json
