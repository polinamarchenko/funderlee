from flask import Flask
from project import db 
from flask_sqlalchemy import SQLAlchemy

StartupsInvestors = db.Table('startups_investors',
    db.Column('id', db.Integer, primary_key=True),
    db.Column('startup_id', db.Integer, db.ForeignKey('startups.id', ondelete="cascade")),
    db.Column('investor_id', db.Integer, db.ForeignKey('investors.id', ondelete="cascade"))
)

class Startup(db.Model):

    __tablename__ = "startups"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    url = db.Column(db.Text)
    investors = db.relationship('Investor', secondary=StartupsInvestors, backref=db.backref('startups', lazy='dynamic'), lazy='dynamic')

    def __init__(self, name, url):
        self.name = name
        self.url = url
