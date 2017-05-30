from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_modus import Modus
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, current_user, login_user, login_required
import os

app = Flask(__name__)
db = SQLAlchemy(app)
login_manager = LoginManager(app)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI') or 'postgres://localhost/funderlee'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

modus = Modus(app)
bcrypt = Bcrypt(app)

from project.startups.views import startups_blueprint
from project.investors.views import investors_blueprint
from project.users.views import users_blueprint
from project.startups.models import Startup
from project.investors.models import Investor
from project.users.models import User
from project.startups.models import StartupsInvestors

app.register_blueprint(startups_blueprint, url_prefix='/startups')
app.register_blueprint(investors_blueprint, url_prefix='/investors')
app.register_blueprint(users_blueprint, url_prefix='/users')

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))
    
@app.route('/')
def root():
    investors = Investor.query.all()
    startups = Startup.query.all()
    return render_template('home.html', investors=investors, startups=startups)
