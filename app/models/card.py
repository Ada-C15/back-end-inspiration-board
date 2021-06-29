from flask import current_app
from app import db
from sqlalchemy.orm import relationship, backref


class Card(db.Model):
    __tablename__ = "card"
    card_id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String)
    likes_count = db.Column(db.Integer)