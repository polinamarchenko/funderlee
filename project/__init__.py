from flask import Flask, redirect, render_template, request, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_modus import Modus
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, current_user, login_user, login_required
from project.collections.forms import CollectionForm
import config
import os

app = Flask(__name__)

if os.environ.get('ENV') == 'production':
    app.config.from_object(config.ProductionConfig())
else:
    app.config.from_object(config.DevelopmentConfig())

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

db = SQLAlchemy(app)
login_manager = LoginManager(app)

modus = Modus(app)
bcrypt = Bcrypt(app)

from project.startups.views import startups_blueprint
from project.investors.views import investors_blueprint
from project.users.views import users_blueprint
from project.startups.models import Startup
from project.investors.models import Investor
from project.users.models import User
from project.startups.models import StartupsInvestors
from project.collections.models import Collection, CollectionInvestor

app.register_blueprint(startups_blueprint, url_prefix='/startups')
app.register_blueprint(investors_blueprint, url_prefix='/investors')
app.register_blueprint(users_blueprint, url_prefix='/users')
# app.register_blueprint(collections_blueprint, url_prefix='/collections')


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.route('/', methods=['GET', 'POST'])
def root():
    investors = Investor.query.all()
    startups = Startup.query.all()
    if request.method == 'POST':
        form = CollectionForm(request.form)
        if form.validate():
            collection = Collection(name=form.name.data, user_id=current_user.id)
            db.session.add(collection)
            db.session.commit()
            flash('You have create a new collection')
            return render_template('home.html', investors=investors, startups=startups)
        flash('Collection name cannot be empty')
        return redirect('url_for(users.new)', form=form)
    return render_template('home.html', investors=investors, startups=startups)
