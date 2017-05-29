from flask import Flask
from project import db
from flask_sqlalchemy import SQLAlchemy

class Investor(db.Model):

    __tablename__ = "investors"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    url = db.Column(db.Text)
    country = db.Column(db.Text)

    def __init__(self, name, url, country):
        self.name = name
        self.url = url
        self.country = country
