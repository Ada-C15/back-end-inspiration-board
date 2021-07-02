from app import db

class Card(db.Model):
    card_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    message = db.Column(db.String)
    like_count = db.Column(db.Integer, default=0)
    board_id = db.Column(db.Integer, db.ForeignKey('board.board_id'))
    
    def to_json(self):
        card =  {
            "id": self.card_id,
            "message": self.message,
            "like_count": self.like_count
        }
        if self.board_id:
            card["board_id"] = self.board_id
        return card