from flask import Flask
from project import db

from flask_sqlalchemy import SQLAlchemy

CollectionInvestor = db.Table('collection_investors',
    db.Column('id', db.Integer, primary_key=True),
    db.Column('collection_id', db.Integer, db.ForeignKey('collections.id', ondelete="cascade")),
    db.Column('investor_id', db.Integer, db.ForeignKey('investors.id', ondelete="cascade"))
)

class Collection(db.Model):

    __tablename__ = "collections"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    name = db.Column(db.Text, unique=True)

    def __init__(self, user_id, name):
        self.user_id = user_id
        self.name = name
