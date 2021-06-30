from app import db

class Board(db.Model):
    board_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    owner = db.Column(db.String)
    cards = db.relationship('Card', backref='board', lazy=True)


    @classmethod
    def from_dict(cls, board_dict): 
        return Board (title = board_dict["title"], 
                owner = board_dict["owner"])

    def as_json(self):
        return {
            "board_id": self.board_id,
            "title": self.title,
            "owner": self.owner,
            "cards": [card.as_json() for card in self.cards],

        }





