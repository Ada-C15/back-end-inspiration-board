# from flask import current_app ? no longer sure about why we needed this here
from app import db

class Board(db.Model):
    board_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    owner = db.Column(db.String, nullable=False)
    cards = db.relationship('Card', backref='card', lazy=True)


# "Every time the API sends back data about a board, the HTTP response includes these key-value pairs": 
# {
#     "board_id": ...,
#     "title": ...,
#     "owner": ...
# }
# Then...
# the method below is to return one board in json format:

def board_to_json_format(self):
    return {
            'board_id': self.board_id,
            'title': self.title,
            'owner': self.owner,
            }


# "Lists of cards are in an array:"
# [
#     {
#         "card_id": ...,
#         "message": ...,
#         "likes_count": ...,
#         "board_id": ...
#     },
#     {
#         "card_id": ...,
#         "message": ...,
#         "likes_count": ...,
#         "board_id": ...
#     }
# ]
# Then...
# the method below is to return an array in json format:

def cards_list_in_board_to_json_format(self):
    # return [c.card_to_json_format() for c in self.cards]
    cards_list = []
    for card in self.cards:
        cards_list.append(card.card_to_json_format()) 
    return cards_list

