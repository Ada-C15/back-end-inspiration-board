'''
  Card Model - 
    - constructor
    - to_dict which formats info into a dict for response
'''
from app import db

class Card(db.Model):
  card_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  message = db.Column(db.String)
  likes_count = db.Column(db.Integer, default=0)
  board_id = db.Column(db.Integer, db.ForeignKey('board.board_id'))

  def to_dict(self):
    return {
      "id" : self.card_id,
      "message" : self.message,
      "likes" : self.likes_count,
    }