from flask import current_app
from app import db
from sqlalchemy.orm import relationship, backref


class Board(db.Model):
    __tablename__ = "board"
    board_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    owner = db.Column(db.String)
