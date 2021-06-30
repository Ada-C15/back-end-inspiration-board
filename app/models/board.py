'''
  Board Model - 
    - constructor
    - to_dict which formats info into a dict for response
'''
from app import db

class Board(db.Model):
  board_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  title = db.Column(db.String)
  owner = db.Column(db.String)
  cards = db.relationship('Card', backref='board', lazy=True)

  def to_dict(self):
    return{
      "id" : self.board_id,
      "title" : self.title,
      "owner" : self.owner,
      "cards" : [card.to_dict() for card in self.cards],
    }
