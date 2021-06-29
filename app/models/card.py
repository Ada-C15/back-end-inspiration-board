from app import db

class Card(db.Model):
    card_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    message = db.Column(db.String)
    like_count = db.Column(db.Integer)
    board_id = db.Column(db.Integer, db.ForeignKey('board.board_id'))
    
    def to_json(self):
        card =  {
            "id": self.card_id,
            "message": self.message,
            "like_count": self.like_count,
            "is_complete": bool(self.completed_at)
        }
        if self.board_id:
            card["board_id"] = self.board_id
        return card