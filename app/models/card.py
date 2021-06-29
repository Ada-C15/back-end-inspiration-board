from app import db



class Card(db.Model):
    card_id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String)
    likes_count = db.Column(db.Integer)
    board_id = db.Column(db.Integer, db.ForeignKey('board.board_id'))
   
    @classmethod
    def from_json(cls, card_dict): 
        return Card (message = card_dict["message"],
            likes_count=0,
             board_id = card_dict["board_id"])

    def as_json(self): 
        return {
            "card_id": self.card_id,
            "message": self.message,
            "likes_count": self.likes_count,
            "board_id": self.board_id,

        }
    
    