from project import db, bcrypt
from flask_login import UserMixin

UsersInvestors = db.Table('users_investors',
    db.Column('id', db.Integer, primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('users.id', ondelete="cascade")),
    db.Column('investor_id', db.Integer, db.ForeignKey('investors.id', ondelete="cascade"))
)

class User(db.Model, UserMixin):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, unique=True)
    email = db.Column(db.Text)
    password = db.Column(db.Text)
    collections = db.relationship('Collection', backref='user')
    investors = db.relationship('Investor', secondary=UsersInvestors, backref=db.backref('users', lazy='dynamic'), lazy='dynamic')

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = bcrypt.generate_password_hash(password).decode('UTF-8')
