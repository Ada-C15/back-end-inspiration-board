from app import db

class Card(db.Model):
    card_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    message = db.Column(db.String, nullable=False)
    likes_count = db.Column(db.Integer, nullable=False) # autoincrement=True?
    board = db.Column(db.Integer, db.ForeignKey('board.board_id')) # nullable=False?


# "When the API sends back a card, the HTTP response looks like:"
# {
#     "card_id": ...,
#     "message": ...,
#     "likes_count": ...,
#     "board_id": ...
# }
# Then...
# the method below is to return a card in json format:

# def card_to_json_format(self):
#     card_to_json = {
#         'card_id': self.card_id,
#         'message': self.message,
#         'likes_count': self.likes_count,
#         'board_id': self.board,
#     }