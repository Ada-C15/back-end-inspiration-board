from app import db

class Card(db.Model):
    card_id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String)
    likes_count = db.Column(db.Integer)
    # child
    board_id = db.Column(db.Integer, db.ForeignKey('board_id.id'))
