from project import db, bcrypt
from flask_login import UserMixin

class User(db.Model, UserMixin):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, unique=True)
    email = db.Column(db.Text)
    password = db.Column(db.Text)
    collections = db.relationship('Collection', backref='user')

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = bcrypt.generate_password_hash(password).decode('UTF-8')
