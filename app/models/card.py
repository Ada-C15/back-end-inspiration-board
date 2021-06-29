from app import db
from flask import current_app

class Card(db.Model):
    __tablename__="card"
    card_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    message = db.Column(db.String(40))
    likes_count = db.Column(db.Integer)
