# from flask import current_app ? no longer sure about why we needed this here
from app import db

# Board, table name: board
# board_id, int, primary key
# title, string
# owner, string

class Board(db.Model):
    board_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    owner = db.Column(db.String, nullable=False)
    # cards = db.relationship('Card', backref='card', lazy=True)



# =========================================================================


# not sure if these will be necessary but just in case we need them later:

# def board_to_json_format(self):
#     return {
#             "id": self.board_id,
#             "title": self.title,
#             "owner": self.owner,
#             }


# def add_cards_response_to_json(self):
#         return {
#             "id": self.board_id,
#             "cards_ids": [c.card_id for c in self.cards]
#         }


# def cards_list_in_board_to_json_format(self):
#     return {
#         "id": self.goal_id,
#         "title": self.title,
#         "cards": [c.card_to_json_format() for c in self.cards]
#     }
