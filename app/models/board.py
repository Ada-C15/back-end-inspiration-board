from app import db
from sqlalchemy.orm import relationship, backref

class Board(db.Model):

    __tablename__ = "boards"
    board_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    owner = db.Column(db.String, nullable=False)
    cards = db.relationship('Card', backref='cards', lazy=True)


    def board_to_json(self):
        return {
                'board_id': self.board_id,
                'title': self.title,
                'owner': self.owner,
                }


    def cards_list_to_json(self):
        # return [c.card_to_json_format() for c in self.cards]
        all_cards = []
        for card in self.cards:
            all_cards.append(card.card_to_json()) 
        return all_cards

