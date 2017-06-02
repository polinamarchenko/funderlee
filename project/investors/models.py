from flask import Flask
from project import db
from flask_sqlalchemy import SQLAlchemy


InvestorsMarkets = db.Table('investors_markets',
    db.Column('id', db.Integer, primary_key=True),
    db.Column('investor_id', db.Integer, db.ForeignKey('investors.id', ondelete="cascade")),
    db.Column('market_id', db.Integer, db.ForeignKey('markets.id', ondelete="cascade"))
)

class Market(db.Model):

    __tablename__ = "markets"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)

    def __init__(self, name):
        self.name = name

class Investor(db.Model):

    __tablename__ = "investors"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    url = db.Column(db.Text)
    country = db.Column(db.Text)
    markets = db.relationship('Market', secondary=InvestorsMarkets, backref=db.backref('investors', lazy='dynamic'), lazy='dynamic')

    def __init__(self, name, url, country):
        self.name = name
        self.url = url
        self.country = country

    def get_market_names(self):
        return ", ".join([market.name for market in self.markets])

    @classmethod
    def get_investors_in_market(cls, market_name):
        return db.session.query(Investor,InvestorsMarkets,Market).filter(Investor.id==InvestorsMarkets.c.investor_id).filter(InvestorsMarkets.c.market_id==Market.id).filter(Market.name==market_name)
        #Investor.query.join
